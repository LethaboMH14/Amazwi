"""Tests for app/arcade.py -- the engagement layer.

Run against real PostgreSQL (see tests/conftest.py): the leaderboard and
deck summaries are real GROUP BY aggregations over joins, and the peer
list depends on the partial-index semantics of `verifier_qualifications`.

The tests that matter most here are not the happy paths. They are:

* `test_progression_is_derived_not_stored` -- proves a level cannot be
  set, only earned.
* `test_leaderboard_ties_break_deterministically` -- doctrine rule 5.
* `test_no_fabricated_engagement_metrics` -- a source-level assertion
  that the module never grows a fake skill radar or a fake presence
  count, which is the specific dishonesty this screen invites.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest

from app.arcade import (
    LEVEL_COEFFICIENT,
    XP_PER_COMPLETED_VERIFICATION,
    XP_PER_VERIFIED_CONTRIBUTION,
    build_decks,
    build_invitations,
    build_leaderboard,
    build_peer_list,
    build_verification_queue,
    build_progression,
    build_quests,
    compute_xp,
    earned_cents,
    level_for_xp,
    progression_for_user,
    speaker_outcomes,
    tier_for_verified_count,
    xp_to_reach_level,
)
from app.models import (
    Assignment,
    AssignmentMode,
    Campaign,
    Card,
    Contribution,
    ContributionState,
    RewardEvent,
    User,
    VerifierQualification,
)

NOW = datetime(2026, 9, 2, 12, 0, tzinfo=timezone.utc)


# --- helpers ----------------------------------------------------------


def _user(db_session, subject: str, name: str | None, languages=("zu",)) -> User:
    user = User(
        provider_subject=subject,
        declared_languages=list(languages),
        display_name=name,
    )
    db_session.add(user)
    db_session.flush()
    return user


def _campaign(db_session, language="zu") -> Campaign:
    campaign = Campaign(
        name=f"campaign-{language}-{uuid.uuid4().hex[:6]}",
        language=language,
        budget_cents=100_000,
        funded_cents=50_000,
        committed_cents=0,
    )
    db_session.add(campaign)
    db_session.flush()
    return campaign


def _card(db_session, campaign: Campaign) -> Card:
    card = Card(
        language=campaign.language,
        target="indiza",
        blocked_words=["ndiza", "isibhakabhaka", "uhambo", "inkundla"],
        accepted_answers=["indiza", "ibhanoyi"],
        distractors=["imoto", "isitimela", "umkhumbi"],
        campaign_id=campaign.id,
    )
    db_session.add(card)
    db_session.flush()
    return card


def _contribution(
    db_session, speaker: User, card: Card, state: ContributionState, created_at=NOW
) -> Contribution:
    contribution = Contribution(
        speaker_id=speaker.id,
        card_id=card.id,
        declared_language=card.language,
        state=state,
        created_at=created_at,
    )
    db_session.add(contribution)
    db_session.flush()
    return contribution


# --- pure progression maths ------------------------------------------


def test_level_one_costs_nothing_and_thresholds_are_the_documented_curve():
    assert xp_to_reach_level(1) == 0
    assert xp_to_reach_level(2) == LEVEL_COEFFICIENT * 2 * 1
    assert xp_to_reach_level(3) == LEVEL_COEFFICIENT * 3 * 2


def test_level_for_xp_is_the_exact_inverse_of_the_threshold_curve():
    # Every boundary, and every point either side of it, for a wide range
    # -- a closed-form seed plus correction must not be off by one.
    for level in range(1, 60):
        floor_xp = xp_to_reach_level(level)
        assert level_for_xp(floor_xp) == level
        if floor_xp > 0:
            assert level_for_xp(floor_xp - 1) == level - 1


def test_level_for_xp_rejects_negative_xp():
    with pytest.raises(ValueError):
        level_for_xp(-1)


def test_tier_boundaries_are_exact():
    assert tier_for_verified_count(0) == "Beginner"
    assert tier_for_verified_count(1) == "Beginner"
    assert tier_for_verified_count(2) == "Amateur"
    assert tier_for_verified_count(4) == "Amateur"
    assert tier_for_verified_count(5) == "Veteran"
    assert tier_for_verified_count(10) == "Expert"
    assert tier_for_verified_count(20) == "Master"
    assert tier_for_verified_count(50) == "Grand Master"
    assert tier_for_verified_count(5000) == "Grand Master"


def test_xp_weights_speaking_above_verifying():
    assert XP_PER_VERIFIED_CONTRIBUTION > XP_PER_COMPLETED_VERIFICATION
    assert compute_xp(1, 0) == XP_PER_VERIFIED_CONTRIBUTION
    assert compute_xp(0, 1) == XP_PER_COMPLETED_VERIFICATION
    assert compute_xp(2, 3) == 2 * 100 + 3 * 25


def test_percent_into_level_never_exceeds_one_hundred():
    for verified in range(0, 40):
        for verifications in range(0, 10):
            progression = build_progression(verified, verifications)
            assert 0 <= progression.percent_into_level <= 100
            assert progression.xp_into_level < progression.xp_for_next_level


# --- derived from real rows -------------------------------------------


def test_progression_is_derived_not_stored(db_session):
    """A level cannot be assigned -- only earned by real verified rows."""
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-speaker", "Nomsa")

    assert progression_for_user(db_session, speaker.id).xp == 0

    _contribution(db_session, speaker, card, ContributionState.CORPUS_ELIGIBLE)
    db_session.flush()
    assert progression_for_user(db_session, speaker.id).xp == 100

    # An UNVALIDATED clip earns nothing: peers did not agree.
    _contribution(db_session, speaker, card, ContributionState.UNVALIDATED)
    db_session.flush()
    assert progression_for_user(db_session, speaker.id).xp == 100
    assert progression_for_user(db_session, speaker.id).verified_contributions == 1


def test_speaker_outcomes_replaces_a_skill_radar_with_the_real_split(db_session):
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-outcomes", "Thabo")

    _contribution(db_session, speaker, card, ContributionState.CORPUS_ELIGIBLE)
    _contribution(db_session, speaker, card, ContributionState.UNVALIDATED)
    _contribution(db_session, speaker, card, ContributionState.OPEN)
    db_session.flush()

    _contribution(db_session, speaker, card, ContributionState.EXPIRED)
    db_session.flush()

    outcomes = speaker_outcomes(db_session, speaker.id)
    assert outcomes.understood == 1
    assert outcomes.not_understood == 1
    assert outcomes.awaiting_peers == 1
    assert outcomes.closed == 1, "EXPIRED is a closed outcome, not still waiting"
    assert outcomes.total == 4


def test_earned_cents_reads_the_reward_ledger(db_session):
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-earn", "Lerato")
    contribution = _contribution(
        db_session, speaker, card, ContributionState.CORPUS_ELIGIBLE
    )
    assert earned_cents(db_session, speaker.id) == 0

    db_session.add(
        RewardEvent(
            contribution_id=contribution.id,
            user_id=speaker.id,
            type="SPEAKER_HONORARIUM",
            amount_cents=200,
            idempotency_key=f"reward-{contribution.id}",
        )
    )
    db_session.flush()
    assert earned_cents(db_session, speaker.id) == 200


def test_leaderboard_ranks_by_verified_contributions(db_session):
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    top = _user(db_session, "sub-top", "Sipho")
    mid = _user(db_session, "sub-mid", "Ayanda")

    for _ in range(3):
        _contribution(db_session, top, card, ContributionState.CORPUS_ELIGIBLE)
    _contribution(db_session, mid, card, ContributionState.CORPUS_ELIGIBLE)
    db_session.flush()

    rows = build_leaderboard(db_session, language="zu", current_user_id=mid.id)
    assert [r.display_name for r in rows] == ["Sipho", "Ayanda"]
    assert rows[0].rank == 1 and rows[0].verified_contributions == 3
    assert rows[1].is_current_user is True
    assert rows[0].is_current_user is False


def test_leaderboard_ties_break_deterministically(db_session):
    """Doctrine rule 5: equal scores must still produce one stable order."""
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    users = [_user(db_session, f"sub-tie-{i}", f"Player {i}") for i in range(5)]
    for user in users:
        _contribution(db_session, user, card, ContributionState.CORPUS_ELIGIBLE)
    db_session.flush()

    first = build_leaderboard(db_session, language="zu", current_user_id=users[0].id)
    for _ in range(5):
        again = build_leaderboard(
            db_session, language="zu", current_user_id=users[0].id
        )
        assert [r.user_id for r in again] == [r.user_id for r in first]
    # The documented tie-break is ascending UUID.
    assert [r.user_id for r in first] == sorted(r.user_id for r in first)


def test_leaderboard_is_scoped_to_one_language(db_session):
    zu_campaign = _campaign(db_session, "zu")
    tn_campaign = _campaign(db_session, "tn")
    zu_card = _card(db_session, zu_campaign)
    tn_card = _card(db_session, tn_campaign)
    zulu_speaker = _user(db_session, "sub-zu", "Zanele", languages=("zu",))
    tswana_speaker = _user(db_session, "sub-tn", "Kagiso", languages=("tn",))

    _contribution(db_session, zulu_speaker, zu_card, ContributionState.CORPUS_ELIGIBLE)
    _contribution(db_session, tswana_speaker, tn_card, ContributionState.CORPUS_ELIGIBLE)
    db_session.flush()

    zu_rows = build_leaderboard(
        db_session, language="zu", current_user_id=zulu_speaker.id
    )
    assert [r.display_name for r in zu_rows] == ["Zanele"]


def test_leaderboard_never_exposes_a_provider_subject(db_session):
    """A user with no display_name must not leak their auth subject."""
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    nameless = _user(db_session, "secret-provider-subject-value", None)
    _contribution(db_session, nameless, card, ContributionState.CORPUS_ELIGIBLE)
    db_session.flush()

    rows = build_leaderboard(
        db_session, language="zu", current_user_id=nameless.id
    )
    assert rows[0].display_name == "Anonymous contributor"
    assert "secret-provider-subject-value" not in rows[0].display_name


def test_invitations_are_unanswered_assignments_only(db_session):
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-inv-speaker", "Bongani")
    verifier = _user(db_session, "sub-inv-verifier", "Palesa")
    contribution = _contribution(
        db_session, speaker, card, ContributionState.OPEN
    )

    pending = Assignment(
        contribution_id=contribution.id,
        verifier_id=verifier.id,
        mode=AssignmentMode.PROFICIENT_VERIFIER,
    )
    db_session.add(pending)
    db_session.flush()

    rows = build_invitations(db_session, current_user_id=verifier.id)
    assert len(rows) == 1
    assert rows[0].speaker_name == "Bongani"
    assert rows[0].contribution_id == contribution.id

    # Answering it removes the invitation -- there is no separate
    # invitation record to fall out of sync with the assignment.
    pending.answer_text = "indiza"
    pending.answered_at = NOW
    db_session.flush()
    assert build_invitations(db_session, current_user_id=verifier.id) == []


def test_peer_list_is_the_real_verifier_cohort(db_session):
    campaign = _campaign(db_session)
    reviewer = _user(db_session, "sub-reviewer", "Reviewer")
    me = _user(db_session, "sub-me", "Me")
    peer = _user(db_session, "sub-peer", "Peer")
    revoked = _user(db_session, "sub-revoked", "Revoked Peer")

    for user, revoked_at in ((me, None), (peer, None), (revoked, NOW)):
        db_session.add(
            VerifierQualification(
                user_id=user.id,
                language="zu",
                qualified_at=NOW - timedelta(days=1),
                reviewed_by=reviewer.id,
                revoked_at=revoked_at,
            )
        )
    db_session.flush()

    rows = build_peer_list(db_session, current_user_id=me.id)
    names = [r.display_name for r in rows]
    assert "Peer" in names
    assert "Me" not in names            # never list yourself
    assert "Revoked Peer" not in names  # revoked qualification is not a peer


def test_decks_report_real_counts_not_presence(db_session):
    campaign = _campaign(db_session, "zu")
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-deck", "Deck Speaker")
    _contribution(db_session, speaker, card, ContributionState.CORPUS_ELIGIBLE)
    db_session.flush()

    decks = build_decks(db_session)
    zu = next(d for d in decks if d.language == "zu")
    assert zu.card_count == 1
    assert zu.contributors == 1
    assert zu.verified_contributions == 1


def test_quests_count_only_todays_rows(db_session):
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-quest", "Quester")

    _contribution(db_session, speaker, card, ContributionState.DRAFT, created_at=NOW)
    _contribution(
        db_session,
        speaker,
        card,
        ContributionState.DRAFT,
        created_at=NOW - timedelta(days=2),
    )
    db_session.flush()

    quests = build_quests(db_session, current_user_id=speaker.id, now=NOW)
    speak = next(q for q in quests if q.key == "speak_today")
    assert speak.progress == 1, "yesterday's contribution must not count today"
    assert speak.complete is False


def test_quest_progress_is_capped_at_its_target(db_session):
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    speaker = _user(db_session, "sub-quest-cap", "Overachiever")
    for _ in range(9):
        _contribution(db_session, speaker, card, ContributionState.DRAFT, created_at=NOW)
    db_session.flush()

    speak = next(
        q
        for q in build_quests(db_session, current_user_id=speaker.id, now=NOW)
        if q.key == "speak_today"
    )
    assert speak.progress == speak.target
    assert speak.complete is True


def test_empty_state_is_honest_for_a_brand_new_user(db_session):
    """A new user sees real zeros, never seeded-looking placeholder scores."""
    user = _user(db_session, "sub-new", "Newcomer")
    progression = progression_for_user(db_session, user.id)
    assert progression.xp == 0
    assert progression.level == 1
    assert progression.tier == "Beginner"
    assert earned_cents(db_session, user.id) == 0
    assert speaker_outcomes(db_session, user.id).total == 0
    assert build_invitations(db_session, current_user_id=user.id) == []
    assert build_peer_list(db_session, current_user_id=user.id) == []


def test_every_contribution_state_is_classified():
    """No state may fall through speaker_outcomes' classification.

    Adding a state to the enum without filing it here would silently
    mis-count someone's record, so this fails loudly instead.
    """
    from app.arcade import (
        AWAITING_STATES,
        CLOSED_STATES,
        NOT_UNDERSTOOD_STATES,
        UNDERSTOOD_STATES,
    )

    classified = (
        UNDERSTOOD_STATES | NOT_UNDERSTOOD_STATES | AWAITING_STATES | CLOSED_STATES
    )
    assert classified == set(ContributionState), (
        "unclassified states: " f"{set(ContributionState) - classified}"
    )
    # And the buckets must be disjoint -- no state counted twice.
    total = (
        len(UNDERSTOOD_STATES)
        + len(NOT_UNDERSTOOD_STATES)
        + len(AWAITING_STATES)
        + len(CLOSED_STATES)
    )
    assert total == len(classified)


def test_response_schema_publishes_no_fabricated_metric():
    """Guard the specific dishonesty this screen invites.

    The reference dashboard this layout follows shows a five-axis skill
    radar and a live "N playing" figure. AMAZWI measures neither. This
    inspects the actual published JSON schema -- the thing a client sees
    -- rather than the source prose, so the module can still *explain*
    why those fields are absent without tripping its own guard.
    """
    from app.api_types import ArcadeDashboardResponse

    schema = str(ArcadeDashboardResponse.model_json_schema()).lower()
    for forbidden in (
        "teamwork",
        "creativity",
        "curiosity",
        "discipline",
        "solving",
        "players_online",
        "playing_now",
        "online_count",
        "streak",
    ):
        assert forbidden not in schema, (
            f"'{forbidden}' appeared in the published schema; AMAZWI does not "
            "measure it and must not publish it"
        )


# --- verification queue ordering -------------------------------------
#
# This is the bug that broke the entire two-device walk, so it gets a
# test that fails loudly if the ordering ever reverts.


def _queue_fixture(db_session):
    """A speaker, two qualified verifiers, and three clips awaiting peers."""
    campaign = _campaign(db_session)
    card = _card(db_session, campaign)
    reviewer = _user(db_session, "sub-q-reviewer", "Reviewer")
    speaker = _user(db_session, "sub-q-speaker", "Speaker")
    v1 = _user(db_session, "sub-q-v1", "Verifier One")
    v2 = _user(db_session, "sub-q-v2", "Verifier Two")

    for user in (v1, v2):
        db_session.add(
            VerifierQualification(
                user_id=user.id,
                language="zu",
                qualified_at=NOW - timedelta(days=1),
                reviewed_by=reviewer.id,
            )
        )

    clips = []
    for age_days in (3, 2, 1):  # oldest first
        contribution = _contribution(
            db_session,
            speaker,
            card,
            ContributionState.OPEN,
            created_at=NOW - timedelta(days=age_days),
        )
        # The queue only offers clips whose audio actually exists.
        contribution.audio_key = f"audio/{contribution.id}"
        clips.append(contribution)
    db_session.flush()
    return speaker, v1, v2, clips


def test_queue_is_oldest_first_when_no_clip_has_been_started(db_session):
    """Fairness: the speaker who has waited longest is served first."""
    _, v1, _, clips = _queue_fixture(db_session)
    rows = build_verification_queue(db_session, verifier_id=v1.id)
    assert [r.contribution_id for r in rows] == [c.id for c in clips]


def test_a_started_clip_outranks_every_untouched_one(db_session):
    """The ordering must CONVERGE two verifiers onto the same clip.

    Regression test for the bug that made the two-device walk impossible.
    With pure oldest-first, verifier 1's queue head was a clip verifier 2
    could not see (v2 had already answered it), and v2's head was an
    older untouched clip. The two never worked on the same recording, so
    no clip ever collected the two answers the resolver requires: every
    contribution sat at "1 of 2" forever and no speaker was ever paid.

    Answers-first fixes it. The moment anyone answers a clip, every other
    eligible verifier is steered to that same clip, because it now sorts
    above every untouched one -- however old those are.
    """
    _, v1, v2, clips = _queue_fixture(db_session)
    newest = clips[-1]

    # v1 answers the NEWEST clip -- the one oldest-first would rank last.
    db_session.add(
        Assignment(
            contribution_id=newest.id,
            verifier_id=v1.id,
            mode=AssignmentMode.PROFICIENT_VERIFIER,
            answer_text="ingubo",
            answer_normalised="ingubo",
            matched=True,
            answered_at=NOW,
        )
    )
    db_session.flush()

    rows = build_verification_queue(db_session, verifier_id=v2.id)
    assert rows, "verifier two must still have work"
    assert rows[0].contribution_id == newest.id, (
        "a clip needing ONE more answer must outrank untouched older clips; "
        "otherwise two verifiers never converge and nothing ever resolves"
    )
    assert rows[0].answers_so_far == 1

    # And it must have left v1's own queue -- you cannot answer twice.
    assert newest.id not in {
        r.contribution_id
        for r in build_verification_queue(db_session, verifier_id=v1.id)
    }


def test_queue_ordering_is_deterministic_across_repeated_calls(db_session):
    """Doctrine rule 5 -- no set-traversal nondeterminism in the queue."""
    _, v1, _, _ = _queue_fixture(db_session)
    runs = [
        [r.contribution_id for r in build_verification_queue(db_session, verifier_id=v1.id)]
        for _ in range(5)
    ]
    assert all(run == runs[0] for run in runs)


def test_a_fresh_recording_invites_a_verifier_before_anyone_claims_it(db_session):
    """The alert must fire for a NEW clip, which is the whole point of it.

    Regression test. Invitations used to be built only from existing
    Assignment rows, and an assignment is created only when a verifier
    actively claims a clip. So a speaker recording produced no invitation
    on any device, the "someone just recorded" alert never fired for a
    new recording, and the laptops only discovered work when a human
    navigated or reloaded -- exactly the reload the alert exists to
    remove.
    """
    _, v1, v2, clips = _queue_fixture(db_session)

    for verifier in (v1, v2):
        rows = build_invitations(db_session, current_user_id=verifier.id)
        assert {r.contribution_id for r in rows} == {c.id for c in clips}, (
            "every unclaimed clip awaiting this verifier must be an invitation"
        )
        assert all(r.assignment_id is None for r in rows), (
            "nothing has been claimed yet, so there is no assignment id to report"
        )


def test_claiming_a_clip_does_not_duplicate_its_invitation(db_session):
    """One clip, one invitation -- whether or not it has been claimed."""
    _, v1, _, clips = _queue_fixture(db_session)
    target = clips[0]

    db_session.add(
        Assignment(
            contribution_id=target.id,
            verifier_id=v1.id,
            mode=AssignmentMode.PROFICIENT_VERIFIER,
        )
    )
    db_session.flush()

    rows = build_invitations(db_session, current_user_id=v1.id)
    ids = [r.contribution_id for r in rows]
    assert len(ids) == len(set(ids)), "a claimed clip must not appear twice"
    claimed = next(r for r in rows if r.contribution_id == target.id)
    assert claimed.assignment_id is not None, "a claimed clip reports its assignment"


def test_an_answered_clip_stops_inviting_the_verifier_who_answered(db_session):
    """Answered work must leave your list, or the alert nags forever.

    Uses the NEWEST clip deliberately. A merged list sorted by created_at
    would rank it LAST and the convergence assertion below would fail --
    which is the point: invitations must preserve the queue's
    answers-first order, not re-sort it back into the bug.
    """
    _, v1, v2, clips = _queue_fixture(db_session)
    target = clips[-1]

    db_session.add(
        Assignment(
            contribution_id=target.id,
            verifier_id=v1.id,
            mode=AssignmentMode.PROFICIENT_VERIFIER,
            answer_text="ingubo",
            answer_normalised="ingubo",
            matched=True,
            answered_at=NOW,
        )
    )
    db_session.flush()

    assert target.id not in {
        r.contribution_id for r in build_invitations(db_session, current_user_id=v1.id)
    }
    # ...but verifier two still needs to answer it, and it now outranks
    # the untouched clips because it is one answer from resolving.
    v2_rows = build_invitations(db_session, current_user_id=v2.id)
    assert v2_rows[0].contribution_id == target.id



def test_a_peer_qualified_in_two_languages_is_one_person(db_session):
    """One row per PERSON, not per qualification.

    Regression test. build_peer_list joined verifier_qualifications, which
    holds a row per (user, language), so a peer qualified in both isiZulu
    and Setswana came back twice with the same user id. The desk rendered
    them as two separate people and React warned about duplicate keys --
    correctly, because the key genuinely was not unique. Every demo
    verifier is qualified in both languages, so the whole list was
    doubled. Caught by reading the browser console, not the code.
    """
    campaign = _campaign(db_session)
    _card(db_session, campaign)
    reviewer = _user(db_session, "sub-bi-reviewer", "Reviewer")
    me = _user(db_session, "sub-bi-me", "Me")
    bilingual = _user(db_session, "sub-bi-peer", "Bilingual Peer")

    for user in (me, bilingual):
        for language in ("zu", "tn"):
            db_session.add(
                VerifierQualification(
                    user_id=user.id,
                    language=language,
                    qualified_at=NOW - timedelta(days=1),
                    reviewed_by=reviewer.id,
                )
            )
    db_session.flush()

    rows = build_peer_list(db_session, current_user_id=me.id)
    ids = [r.user_id for r in rows]
    assert ids == [bilingual.id], "one row per person, however many languages"
    assert len(ids) == len(set(ids)), "duplicate user ids break the list key"
    assert rows[0].languages == ["tn", "zu"], "sorted, so the order is stable"


def test_peer_list_is_deterministic_across_repeated_calls(db_session):
    """Doctrine rule 5 -- the collapse must not traverse a set unordered."""
    reviewer = _user(db_session, "sub-det-reviewer", "Reviewer")
    me = _user(db_session, "sub-det-me", "Me")
    peers = [_user(db_session, f"sub-det-{i}", f"Peer {i}") for i in range(5)]
    for user in [me, *peers]:
        for language in ("zu", "tn"):
            db_session.add(
                VerifierQualification(
                    user_id=user.id,
                    language=language,
                    qualified_at=NOW - timedelta(days=1),
                    reviewed_by=reviewer.id,
                )
            )
    db_session.flush()

    runs = [
        [r.user_id for r in build_peer_list(db_session, current_user_id=me.id)]
        for _ in range(5)
    ]
    assert all(run == runs[0] for run in runs)
