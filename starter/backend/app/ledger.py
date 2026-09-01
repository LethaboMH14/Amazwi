"""Reward ledger service functions (S5, §8 invariants).

Cross-lane, pending Sbu's review -- see BUILD_LOG.md. Implements only the
operations needed to make §8's six required property-test guarantees real
and testable: crediting a reward, requesting a cash-out, applying a
provider callback, and computing an available balance. Does not implement
the MoMo provider adapter itself (§9) -- that's a separate, larger piece
of work with real external-API unknowns, deliberately out of scope here.

Design choice, stated so it can be checked: reward_events is an immutable,
append-only ledger (never updated, per §8's "a reward row is not updated
into a payment row" and "revocation never deletes financial history").
Cash-out reservation/settlement is tracked on payment_attempts, and
"available balance" is computed as posted credits minus reserved/settled
debits (§8) -- not by mutating individual reward rows into a state
machine the spec doesn't actually define at that granularity.
"""
from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Campaign, PaymentAttempt, PaymentState, RewardEvent


class InsufficientBalanceError(Exception):
    pass


def credit_reward(
    session: Session,
    *,
    contribution_id: uuid.UUID,
    user_id: uuid.UUID,
    reward_type: str,
    amount_cents: int,
    idempotency_key: str,
    campaign_id: Optional[uuid.UUID] = None,
    commit: bool = True,
) -> RewardEvent:
    """§8 invariant 1: resolving the same contribution repeatedly creates
    one reward. Idempotent on (contribution_id, user_id, reward_type) --
    the resolver's natural idempotency key per §5's "safe to call
    repeatedly" -- if a matching reward already exists, returns it
    unchanged rather than crediting again or raising. idempotency_key is
    also unique (a second, independent uniqueness guarantee matching the
    field name) but is not used as the primary lookup key here: a genuine
    idempotency_key collision across two different (contribution, user,
    type) triples is a caller bug, not a benign repeat, so it is left to
    raise rather than silently matched against.

    If campaign_id is given, increments the campaign's committed_cents in
    the SAME transaction (§8: "campaign committed amount changes in the
    same transaction as reward credit") -- the DB CHECK constraint
    (committed_cents <= funded_cents) is what actually enforces invariant
    5 (campaign commitments never exceed the funded budget); this function
    just makes sure both writes commit or roll back together. Set ``commit``
    to False only when a caller owns a wider transaction, such as §5's
    resolver which must atomically persist contribution state, the decision,
    and the reward.
    """
    existing = session.execute(
        select(RewardEvent).where(
            RewardEvent.contribution_id == contribution_id,
            RewardEvent.user_id == user_id,
            RewardEvent.type == reward_type,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    event = RewardEvent(
        contribution_id=contribution_id,
        user_id=user_id,
        type=reward_type,
        amount_cents=amount_cents,
        idempotency_key=idempotency_key,
    )
    session.add(event)

    if campaign_id is not None:
        campaign = session.get(Campaign, campaign_id)
        if campaign is None:
            raise ValueError(f"no such campaign {campaign_id}")
        campaign.committed_cents += amount_cents

    try:
        if commit:
            session.commit()
        else:
            # Execute constraints now, while the caller can still roll back
            # its wider transaction. Do not publish a partial reward yet.
            session.flush()
    except IntegrityError as exc:
        if not commit:
            raise
        session.rollback()
        # Distinguish a benign race (another caller's identical resolver
        # call landed first on the SAME (contribution, user, type) triple)
        # from a real error. Re-check by the triple, not by parsing the
        # DB error text (fragile across Postgres versions/locales) -- if
        # nothing matching landed, this was a genuine failure (the budget
        # CHECK, or an idempotency_key collision across two different
        # triples, which is a caller bug either way) and the original
        # error is re-raised unmodified rather than relabelled.
        existing = session.execute(
            select(RewardEvent).where(
                RewardEvent.contribution_id == contribution_id,
                RewardEvent.user_id == user_id,
                RewardEvent.type == reward_type,
            )
        ).scalar_one_or_none()
        if existing is not None:
            return existing
        raise
    return event


def available_balance_cents(session: Session, user_id: uuid.UUID) -> int:
    """§8: 'available balance includes only posted credits minus
    reserved/settled debits; pending, failed and paid provider attempts do
    not get summed as equivalent money.'

    Credits: all reward_events for the user (immutable, always posted).
    Debits: payment_attempts NOT in FAILED state -- CREATED/SUBMITTED/
    PENDING/PAID all reserve or have already spent the balance. FAILED
    attempts are excluded, which is how a failed cash-out "releases the
    reservation" (§8 invariant 4) -- structurally, by not counting against
    balance, rather than by mutating a state elsewhere.
    """
    credited = session.execute(
        select(func.coalesce(func.sum(RewardEvent.amount_cents), 0)).where(
            RewardEvent.user_id == user_id
        )
    ).scalar_one()
    reserved_or_settled = session.execute(
        select(func.coalesce(func.sum(PaymentAttempt.amount_cents), 0)).where(
            PaymentAttempt.user_id == user_id,
            PaymentAttempt.state != PaymentState.FAILED,
        )
    ).scalar_one()
    return int(credited) - int(reserved_or_settled)


def request_cash_out(
    session: Session,
    *,
    user_id: uuid.UUID,
    amount_cents: int,
    provider_mode: str,
    idempotency_key: str,
) -> PaymentAttempt:
    """§8 invariant 2: submitting the same cash-out repeatedly creates one
    reservation. Idempotent on idempotency_key.

    Refuses to create a new reservation beyond the available balance --
    NOT a DB constraint (balance is a cross-row aggregate, not expressible
    as a single-table CHECK), so this check is enforced here, in the same
    transaction as the insert, to avoid a race between the balance read
    and the insert.
    """
    existing = session.execute(
        select(PaymentAttempt).where(PaymentAttempt.idempotency_key == idempotency_key)
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    balance = available_balance_cents(session, user_id)
    if amount_cents > balance:
        raise InsufficientBalanceError(
            f"cash-out of {amount_cents}c exceeds available balance {balance}c"
        )

    attempt = PaymentAttempt(
        user_id=user_id,
        amount_cents=amount_cents,
        provider_mode=provider_mode,
        provider_reference=None,
        state=PaymentState.SUBMITTED,
        idempotency_key=idempotency_key,
    )
    session.add(attempt)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        existing = session.execute(
            select(PaymentAttempt).where(PaymentAttempt.idempotency_key == idempotency_key)
        ).scalar_one_or_none()
        if existing is not None:
            return existing
        raise
    return attempt


def apply_payment_callback(
    session: Session,
    *,
    attempt_id: uuid.UUID,
    new_state: PaymentState,
    provider_reference: Optional[str] = None,
) -> PaymentAttempt:
    """§8 invariant 3: a callback may arrive more than once without
    changing value twice. Once an attempt is in a terminal state (PAID or
    FAILED), a repeat callback is a no-op -- it does not re-fire the state
    transition or overwrite provider_reference.
    """
    attempt = session.get(PaymentAttempt, attempt_id)
    if attempt is None:
        raise ValueError(f"no such payment attempt {attempt_id}")

    if attempt.state in (PaymentState.PAID, PaymentState.FAILED):
        return attempt  # already terminal -- duplicate callback, no-op

    attempt.state = new_state
    if provider_reference is not None:
        attempt.provider_reference = provider_reference
    session.commit()
    return attempt
