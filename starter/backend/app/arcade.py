"""Engagement layer: progression, leaderboard, quests and peer invitations.

Every value this module returns is DERIVED FROM REAL ROWS. Nothing here
invents a score. That constraint is the reason two things a conventional
game dashboard would show are deliberately absent:

* **No skill/personality radar.** A five-axis "Teamwork / Creativity /
  Discipline / Curiosity / Solving" chart is the standard ornament on this
  kind of screen, and AMAZWI measures none of those things. Rather than
  fabricate five plausible numbers, `speaker_outcomes` returns the real
  split the database actually holds -- understood, not understood, still
  waiting -- which is the honest shape of the same visual slot.
* **No "N playing now".** Live concurrency is not tracked. `DeckSummary`
  publishes `contributors`, a real distinct-speaker count, instead of a
  presence figure nothing measures.

Determinism (doctrine rule 5): every traversal that feeds a rank is sorted
with an explicit total order, and every tie breaks on the user's UUID, so
the same database state always produces the same leaderboard.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import (
    Assignment,
    Card,
    Contribution,
    ContributionState,
    RewardEvent,
    User,
    VerifierQualification,
)

# --- progression constants -------------------------------------------
# Public and fixed so a receipt can be recomputed by hand. Changing these
# changes every historical level, so they are constants, not config.

XP_PER_VERIFIED_CONTRIBUTION = 100
"""Awarded to the speaker when a clip reaches CORPUS_ELIGIBLE."""

XP_PER_COMPLETED_VERIFICATION = 25
"""Awarded to a verifier for each assignment they actually answered."""

LEVEL_COEFFICIENT = 150
"""Cumulative XP to reach level L is LEVEL_COEFFICIENT * L * (L - 1)."""

TIER_THRESHOLDS: tuple[tuple[int, str], ...] = (
    (50, "Grand Master"),
    (20, "Master"),
    (10, "Expert"),
    (5, "Veteran"),
    (2, "Amateur"),
    (0, "Beginner"),
)
"""Verified-contribution count -> tier name. Descending; first match wins."""


def xp_to_reach_level(level: int) -> int:
    """Cumulative XP required to be *at* `level`. Level 1 costs nothing."""
    if level < 1:
        raise ValueError("level must be >= 1")
    return LEVEL_COEFFICIENT * level * (level - 1)


def level_for_xp(xp: int) -> int:
    """Highest level fully paid for by `xp`.

    Solved directly rather than by looping, so the cost does not grow with
    the player's level: L is the largest integer where 150*L*(L-1) <= xp.
    """
    if xp < 0:
        raise ValueError("xp must be >= 0")
    level = 1
    # Closed-form seed, then correct by at most one step to avoid any
    # floating-point boundary error deciding a player's level.
    seed = int((1 + (1 + 4 * xp / LEVEL_COEFFICIENT) ** 0.5) / 2)
    level = max(1, seed)
    while xp_to_reach_level(level + 1) <= xp:
        level += 1
    while level > 1 and xp_to_reach_level(level) > xp:
        level -= 1
    return level


def tier_for_verified_count(verified: int) -> str:
    if verified < 0:
        raise ValueError("verified must be >= 0")
    for threshold, name in TIER_THRESHOLDS:
        if verified >= threshold:
            return name
    return TIER_THRESHOLDS[-1][1]


def compute_xp(verified_contributions: int, completed_verifications: int) -> int:
    return (
        verified_contributions * XP_PER_VERIFIED_CONTRIBUTION
        + completed_verifications * XP_PER_COMPLETED_VERIFICATION
    )


# --- value objects ----------------------------------------------------


@dataclass(frozen=True)
class Progression:
    xp: int
    level: int
    tier: str
    xp_into_level: int
    xp_for_next_level: int
    verified_contributions: int
    completed_verifications: int

    @property
    def percent_into_level(self) -> int:
        if self.xp_for_next_level <= 0:
            return 0
        return round(100 * self.xp_into_level / self.xp_for_next_level)


def build_progression(verified: int, verifications: int) -> Progression:
    xp = compute_xp(verified, verifications)
    level = level_for_xp(xp)
    floor_xp = xp_to_reach_level(level)
    next_xp = xp_to_reach_level(level + 1)
    return Progression(
        xp=xp,
        level=level,
        tier=tier_for_verified_count(verified),
        xp_into_level=xp - floor_xp,
        xp_for_next_level=next_xp - floor_xp,
        verified_contributions=verified,
        completed_verifications=verifications,
    )


# --- queries ----------------------------------------------------------


def _verified_count(session: Session, user_id: uuid.UUID) -> int:
    return int(
        session.execute(
            select(func.count())
            .select_from(Contribution)
            .where(
                Contribution.speaker_id == user_id,
                Contribution.state == ContributionState.CORPUS_ELIGIBLE,
            )
        ).scalar_one()
    )


def _completed_verifications(session: Session, user_id: uuid.UUID) -> int:
    return int(
        session.execute(
            select(func.count())
            .select_from(Assignment)
            .where(
                Assignment.verifier_id == user_id,
                Assignment.answered_at.is_not(None),
            )
        ).scalar_one()
    )


def progression_for_user(session: Session, user_id: uuid.UUID) -> Progression:
    return build_progression(
        _verified_count(session, user_id),
        _completed_verifications(session, user_id),
    )


def earned_cents(session: Session, user_id: uuid.UUID) -> int:
    """Total credited to this user in the reward ledger.

    Reads `reward_events`, which is the ledger of record. This is money
    *credited*, never money paid out -- payout is a separate, reviewed
    step and this function must never be described as a cash balance.
    """
    total = session.execute(
        select(func.coalesce(func.sum(RewardEvent.amount_cents), 0)).where(
            RewardEvent.user_id == user_id
        )
    ).scalar_one()
    return int(total)


# Explicit classification of every contribution state. A catch-all
# "everything else is pending" bucket would silently mis-file any state
# added later -- VOIDED and EXPIRED in particular are closed outcomes,
# not clips still waiting for peers. `test_every_contribution_state_is
# _classified` fails if a new enum member is not placed here.

UNDERSTOOD_STATES = frozenset({ContributionState.CORPUS_ELIGIBLE})
NOT_UNDERSTOOD_STATES = frozenset({ContributionState.UNVALIDATED})
AWAITING_STATES = frozenset(
    {
        ContributionState.DRAFT,
        ContributionState.RECORDED,
        ContributionState.QUALITY_PASSED,
        ContributionState.OPEN,
        ContributionState.UNDERSTOOD,
        ContributionState.REVIEW_REQUIRED,
    }
)
CLOSED_STATES = frozenset({ContributionState.VOIDED, ContributionState.EXPIRED})


@dataclass(frozen=True)
class SpeakerOutcomes:
    """The real replacement for a fabricated skill radar."""

    understood: int
    not_understood: int
    awaiting_peers: int
    closed: int

    @property
    def total(self) -> int:
        return self.understood + self.not_understood + self.awaiting_peers + self.closed


def speaker_outcomes(session: Session, user_id: uuid.UUID) -> SpeakerOutcomes:
    rows = session.execute(
        select(Contribution.state, func.count())
        .where(Contribution.speaker_id == user_id)
        .group_by(Contribution.state)
    ).all()

    tally = {"understood": 0, "not_understood": 0, "awaiting_peers": 0, "closed": 0}
    for state, count in rows:
        if state in UNDERSTOOD_STATES:
            tally["understood"] += int(count)
        elif state in NOT_UNDERSTOOD_STATES:
            tally["not_understood"] += int(count)
        elif state in AWAITING_STATES:
            tally["awaiting_peers"] += int(count)
        elif state in CLOSED_STATES:
            tally["closed"] += int(count)
        else:  # pragma: no cover -- guarded by a test over the enum
            raise AssertionError(f"unclassified contribution state: {state}")
    return SpeakerOutcomes(**tally)


@dataclass(frozen=True)
class LeaderboardRow:
    rank: int
    user_id: uuid.UUID
    display_name: str
    verified_contributions: int
    xp: int
    tier: str
    is_current_user: bool


def _display_name_for(user: User) -> str:
    """Never leak a provider subject as a fallback name."""
    return user.display_name or "Anonymous contributor"


def build_leaderboard(
    session: Session,
    *,
    language: str,
    current_user_id: uuid.UUID,
    limit: int = 10,
) -> list[LeaderboardRow]:
    """Rank speakers in one language by verified contributions.

    Ties break on the user's UUID so the order is total and stable across
    runs -- two people on 3 clips each always appear in the same order.
    """
    verified_sq = (
        select(
            Contribution.speaker_id.label("user_id"),
            func.count().label("verified"),
        )
        .where(
            Contribution.declared_language == language,
            Contribution.state == ContributionState.CORPUS_ELIGIBLE,
        )
        .group_by(Contribution.speaker_id)
        .subquery()
    )
    rows = session.execute(
        select(User, verified_sq.c.verified)
        .join(verified_sq, verified_sq.c.user_id == User.id)
        .order_by(verified_sq.c.verified.desc(), User.id.asc())
        .limit(limit)
    ).all()

    out: list[LeaderboardRow] = []
    for index, (user, verified) in enumerate(rows, start=1):
        verifications = _completed_verifications(session, user.id)
        progression = build_progression(int(verified), verifications)
        out.append(
            LeaderboardRow(
                rank=index,
                user_id=user.id,
                display_name=_display_name_for(user),
                verified_contributions=int(verified),
                xp=progression.xp,
                tier=progression.tier,
                is_current_user=user.id == current_user_id,
            )
        )
    return out


@dataclass(frozen=True)
class PeerRow:
    user_id: uuid.UUID
    display_name: str
    language: str
    tier: str
    verified_contributions: int


def build_peer_list(
    session: Session, *, current_user_id: uuid.UUID, limit: int = 20
) -> list[PeerRow]:
    """Qualified verifiers the current user shares a language cohort with.

    This is the honest equivalent of a friend list: AMAZWI has no social
    graph, so it publishes the people who can actually verify the caller's
    clips rather than inventing friendships.
    """
    my_languages = [
        row[0]
        for row in session.execute(
            select(VerifierQualification.language)
            .where(
                VerifierQualification.user_id == current_user_id,
                VerifierQualification.revoked_at.is_(None),
            )
            .distinct()
        ).all()
    ]
    if not my_languages:
        my_languages = [
            row[0]
            for row in session.execute(
                select(Contribution.declared_language)
                .where(Contribution.speaker_id == current_user_id)
                .distinct()
            ).all()
        ]
    if not my_languages:
        return []

    rows = session.execute(
        select(User, VerifierQualification.language)
        .join(VerifierQualification, VerifierQualification.user_id == User.id)
        .where(
            VerifierQualification.language.in_(sorted(my_languages)),
            VerifierQualification.revoked_at.is_(None),
            User.id != current_user_id,
        )
        .order_by(VerifierQualification.language.asc(), User.id.asc())
        .limit(limit)
    ).all()

    out: list[PeerRow] = []
    for user, language in rows:
        verified = _verified_count(session, user.id)
        out.append(
            PeerRow(
                user_id=user.id,
                display_name=_display_name_for(user),
                language=language,
                tier=tier_for_verified_count(verified),
                verified_contributions=verified,
            )
        )
    return out


@dataclass(frozen=True)
class InvitationRow:
    """A pending peer-verification request.

    This is the real thing a "duel invitation" card represents: another
    speaker is waiting for this user to listen and answer. Accepting is
    answering the assignment; there is no separate invitation record and
    none is invented here.

    `assignment_id` is None when the clip is waiting for this verifier but
    has not been claimed yet. That case is the common one -- and missing
    it was a bug: invitations used to require an existing Assignment row,
    which only appears once a verifier actively claims a clip. A speaker
    recording therefore produced NO invitation on anyone's device, so the
    "someone just recorded" alert could never fire for a new recording.
    The one thing it existed to announce was the one thing it could not.
    """

    assignment_id: uuid.UUID | None
    contribution_id: uuid.UUID
    language: str
    speaker_name: str
    created_at: datetime


def build_invitations(
    session: Session, *, current_user_id: uuid.UUID, limit: int = 10
) -> list[InvitationRow]:
    speaker = User.__table__.alias("speaker")
    rows = session.execute(
        select(
            Assignment.id,
            Contribution.id,
            Contribution.declared_language,
            speaker.c.display_name,
            Contribution.created_at,
        )
        .join(Contribution, Contribution.id == Assignment.contribution_id)
        .join(speaker, speaker.c.id == Contribution.speaker_id)
        .where(
            Assignment.verifier_id == current_user_id,
            Assignment.answered_at.is_(None),
        )
        .order_by(Contribution.created_at.asc(), Assignment.id.asc())
        .limit(limit)
    ).all()
    invitations = [
        InvitationRow(
            assignment_id=assignment_id,
            contribution_id=contribution_id,
            language=language,
            speaker_name=display_name or "Anonymous contributor",
            created_at=created_at,
        )
        for assignment_id, contribution_id, language, display_name, created_at in rows
    ]

    # Unclaimed work counts as an invitation too. Without this the list
    # only ever showed clips this verifier had ALREADY opened, so a fresh
    # recording was invisible until someone navigated to the verify screen
    # and claimed it by hand -- which is precisely the reload the live
    # alert is supposed to remove.
    claimed = {row.contribution_id for row in invitations}
    for queued in build_verification_queue(
        session, verifier_id=current_user_id, limit=limit
    ):
        if queued.contribution_id in claimed:
            continue
        invitations.append(
            InvitationRow(
                assignment_id=None,
                contribution_id=queued.contribution_id,
                language=queued.language,
                speaker_name=queued.speaker_name,
                created_at=queued.created_at,
            )
        )

    # Order is concatenation, NOT a re-sort. Sorting the merged list by
    # created_at would silently undo the queue's answers-first ordering
    # and put the convergence bug straight back: an untouched older clip
    # would outrank one that needs a single further answer to resolve.
    #
    # So: work you already opened comes first (finish what you started),
    # then queued work in queue order. Both sources are individually
    # totally ordered and deterministic, so the concatenation is too
    # (doctrine rule 5).
    return invitations[:limit]


@dataclass(frozen=True)
class DeckSummary:
    """One language deck. `contributors` is a real distinct-speaker count."""

    language: str
    card_count: int
    contributors: int
    verified_contributions: int


def build_decks(session: Session) -> list[DeckSummary]:
    languages = [
        row[0]
        for row in session.execute(
            select(Card.language).distinct().order_by(Card.language.asc())
        ).all()
    ]
    out: list[DeckSummary] = []
    for language in languages:
        card_count = int(
            session.execute(
                select(func.count()).select_from(Card).where(Card.language == language)
            ).scalar_one()
        )
        contributors = int(
            session.execute(
                select(func.count(func.distinct(Contribution.speaker_id))).where(
                    Contribution.declared_language == language
                )
            ).scalar_one()
        )
        verified = int(
            session.execute(
                select(func.count())
                .select_from(Contribution)
                .where(
                    Contribution.declared_language == language,
                    Contribution.state == ContributionState.CORPUS_ELIGIBLE,
                )
            ).scalar_one()
        )
        out.append(
            DeckSummary(
                language=language,
                card_count=card_count,
                contributors=contributors,
                verified_contributions=verified,
            )
        )
    return out


# --- daily quests -----------------------------------------------------

QUEST_SPEAK_TARGET = 2
QUEST_VERIFY_TARGET = 2
QUEST_SPEAK_XP = 140
QUEST_VERIFY_XP = 250


@dataclass(frozen=True)
class QuestRow:
    key: str
    label: str
    detail: str
    progress: int
    target: int
    reward_xp: int

    @property
    def complete(self) -> bool:
        return self.progress >= self.target


def _day_bounds(now: datetime) -> tuple[datetime, datetime]:
    """UTC day window for `now`, returned as aware datetimes."""
    current = now.astimezone(timezone.utc)
    start = datetime.combine(current.date(), time.min, tzinfo=timezone.utc)
    return start, start + timedelta(days=1)


def build_quests(
    session: Session, *, current_user_id: uuid.UUID, now: datetime
) -> list[QuestRow]:
    """Daily quests measured against rows actually written today.

    Progress is a count of real contributions and real answered
    assignments in the current UTC day -- not a stored counter that could
    drift from the ledger.
    """
    start, end = _day_bounds(now)

    spoke = int(
        session.execute(
            select(func.count())
            .select_from(Contribution)
            .where(
                Contribution.speaker_id == current_user_id,
                Contribution.created_at >= start,
                Contribution.created_at < end,
            )
        ).scalar_one()
    )
    verified = int(
        session.execute(
            select(func.count())
            .select_from(Assignment)
            .where(
                Assignment.verifier_id == current_user_id,
                Assignment.answered_at.is_not(None),
                Assignment.answered_at >= start,
                Assignment.answered_at < end,
            )
        ).scalar_one()
    )

    return [
        QuestRow(
            key="speak_today",
            label=f"Record {QUEST_SPEAK_TARGET} voice cards",
            detail="Describe the word without saying it.",
            progress=min(spoke, QUEST_SPEAK_TARGET),
            target=QUEST_SPEAK_TARGET,
            reward_xp=QUEST_SPEAK_XP,
        ),
        QuestRow(
            key="verify_today",
            label=f"Listen to {QUEST_VERIFY_TARGET} peers",
            detail="Type what you understood, independently.",
            progress=min(verified, QUEST_VERIFY_TARGET),
            target=QUEST_VERIFY_TARGET,
            reward_xp=QUEST_VERIFY_XP,
        ),
    ]


# --- verification queue ------------------------------------------------


@dataclass(frozen=True)
class QueueRow:
    """A contribution this verifier could pick up right now."""

    contribution_id: uuid.UUID
    language: str
    speaker_name: str
    created_at: datetime
    answers_so_far: int


def build_verification_queue(
    session: Session, *, verifier_id: uuid.UUID, limit: int = 10
) -> list[QueueRow]:
    """Contributions awaiting THIS verifier, closest-to-resolving first.

    Exists because the two-device walk was impossible without it: the
    verifier route needed a contribution id in the URL, and nothing gave
    the verifier laptop that id. In a demo it meant reading a UUID off a
    phone and typing it into a laptop; in the real product it meant the
    queue did not exist at all.

    Ordered by answers already collected (descending), then oldest
    first. See the comment on the order_by for why that ordering is the
    difference between a working two-device walk and a queue where no
    clip ever reaches the two answers the resolver needs.

    Filters mirror `cohorts.select_next_verifier` so a row that appears
    here can actually be claimed:
      * the verifier is qualified and not revoked in that language
      * they are not the speaker
      * they do not already hold an assignment for it
      * the clip still needs answers (fewer than two)
    """
    my_languages = [
        row[0]
        for row in session.execute(
            select(VerifierQualification.language)
            .where(
                VerifierQualification.user_id == verifier_id,
                VerifierQualification.revoked_at.is_(None),
            )
            .distinct()
        ).all()
    ]
    if not my_languages:
        return []

    mine = (
        select(Assignment.contribution_id)
        .where(Assignment.verifier_id == verifier_id)
        .scalar_subquery()
    )
    answered = (
        select(
            Assignment.contribution_id.label("cid"),
            func.count().label("n"),
        )
        .where(Assignment.answered_at.is_not(None))
        .group_by(Assignment.contribution_id)
        .subquery()
    )

    speaker = User.__table__.alias("speaker")
    rows = session.execute(
        select(
            Contribution.id,
            Contribution.declared_language,
            speaker.c.display_name,
            Contribution.created_at,
            func.coalesce(answered.c.n, 0),
        )
        .join(speaker, speaker.c.id == Contribution.speaker_id)
        .outerjoin(answered, answered.c.cid == Contribution.id)
        .where(
            Contribution.declared_language.in_(sorted(my_languages)),
            Contribution.speaker_id != verifier_id,
            Contribution.id.not_in(mine),
            Contribution.audio_key.is_not(None),
            func.coalesce(answered.c.n, 0) < 2,
        )
        # ORDERING IS LOAD-BEARING, and getting it wrong broke the whole
        # two-verifier walk. Pure oldest-first let two verifiers work on
        # DIFFERENT clips forever: verifier 1's head was a clip verifier 2
        # could not see (already answered by 2), so no clip ever collected
        # the two answers the resolver requires. Measured on the live
        # server: V1's queue head was 38465f76 while V2's was d903cf4b.
        #
        # Answers-first fixes it by making the rule CONVERGENT -- the moment
        # anyone answers a clip, every other eligible verifier is steered to
        # that same clip, because it now sorts above every untouched one.
        # A clip needing one more answer is also the most valuable work
        # available: it is one answer away from paying its speaker.
        #
        # Oldest-first is preserved as the tie-break, so the original
        # fairness property (longest wait served first) still holds among
        # clips at the same stage. Both keys are total and deterministic.
        .order_by(
            func.coalesce(answered.c.n, 0).desc(),
            Contribution.created_at.asc(),
            Contribution.id.asc(),
        )
        .limit(limit)
    ).all()

    return [
        QueueRow(
            contribution_id=cid,
            language=language,
            speaker_name=name or "Anonymous contributor",
            created_at=created,
            answers_so_far=int(n),
        )
        for cid, language, name, created, n in rows
    ]
