"""Tests for app/rewards.py -- the redemption catalogue.

The important tests here are not "does it list three items". They are
the ones that stop this screen from lying:

* `test_demo_provider_can_never_present_a_redeemable_item` -- the whole
  point of deriving availability instead of storing it.
* `test_catalogue_names_no_merchant_or_prize_draw` -- the reference
  design lists retailer discounts and a phone giveaway; AMAZWI has
  neither relationship, and this fails if one is ever added.
* `test_no_parallel_points_currency` -- the ledger is rand cents, and a
  second money field would be a second source of truth.
"""
from __future__ import annotations

import uuid

import pytest

from app.rewards import (
    CATALOGUE,
    Availability,
    availability_for,
    build_catalogue,
    is_live_provider,
)
from app.models import Campaign, Card, Contribution, ContributionState, RewardEvent, User


def _user(db_session, subject="sub-rewards", name="Rewards User") -> User:
    user = User(provider_subject=subject, declared_languages=["zu"], display_name=name)
    db_session.add(user)
    db_session.flush()
    return user


def _credit(db_session, user: User, cents: int, seq: int = 0) -> None:
    campaign = Campaign(
        name=f"c-{uuid.uuid4().hex[:6]}",
        language="zu",
        budget_cents=100_000,
        funded_cents=50_000,
        committed_cents=0,
    )
    db_session.add(campaign)
    db_session.flush()
    card = Card(
        language="zu",
        target="indiza",
        blocked_words=["ndiza", "isibhakabhaka", "uhambo", "inkundla"],
        accepted_answers=["indiza", "ibhanoyi"],
        distractors=["imoto", "isitimela", "umkhumbi"],
        campaign_id=campaign.id,
    )
    db_session.add(card)
    db_session.flush()
    contribution = Contribution(
        speaker_id=user.id,
        card_id=card.id,
        declared_language="zu",
        state=ContributionState.CORPUS_ELIGIBLE,
    )
    db_session.add(contribution)
    db_session.flush()
    db_session.add(
        RewardEvent(
            contribution_id=contribution.id,
            user_id=user.id,
            type="SPEAKER_HONORARIUM",
            amount_cents=cents,
            idempotency_key=f"reward-{contribution.id}-{seq}",
        )
    )
    db_session.flush()


# --- the honesty guarantees ------------------------------------------


def test_demo_provider_can_never_present_a_redeemable_item(db_session):
    """Structural, not conventional: availability is derived each build."""
    user = _user(db_session)
    _credit(db_session, user, 100_000)  # far above every threshold

    view = build_catalogue(db_session, user_id=user.id, provider_mode="demo")

    assert view.provider_connected is False
    assert view.any_redeemable is False
    assert {r.availability for r in view.rows} == {
        Availability.PROVIDER_NOT_CONNECTED
    }, "a demo provider must not offer redemption at any balance"


@pytest.mark.parametrize(
    "mode", ["demo", "sandbox", "mock", "staging", "test", "", "  ", "DEMO"]
)
def test_only_an_explicitly_live_provider_counts_as_connected(mode):
    """Allowlist, not blocklist: a new mode is not live by default."""
    assert is_live_provider(mode) is False


@pytest.mark.parametrize("mode", ["live", "production", "LIVE", " Production "])
def test_live_modes_are_recognised(mode):
    assert is_live_provider(mode) is True


def test_catalogue_names_no_merchant_or_prize_draw():
    """The reference design lists retailer discounts and a giveaway.

    AMAZWI has neither relationship. Every item must map to a product
    MTN MoMo actually operates.
    """
    text = " ".join(
        f"{i.key} {i.title} {i.description} {i.momo_product}" for i in CATALOGUE
    ).lower()
    for forbidden in (
        "nishat",
        "iphone",
        "lucky draw",
        "giveaway",
        "% off",
        "discount at",
        "voucher code",
        "slots left",
    ):
        assert forbidden not in text, f"'{forbidden}' implies a relationship we do not have"


def test_no_parallel_points_currency():
    """One money unit. The ledger is rand cents."""
    from app.api_types import RewardsResponse

    schema = str(RewardsResponse.model_json_schema()).lower()
    for forbidden in ("points", "coins", "gems", "tokens_balance"):
        assert forbidden not in schema


def test_catalogue_item_has_no_settable_availability_flag():
    """Availability cannot be stored wrongly because it cannot be stored."""
    from dataclasses import fields

    names = {f.name for f in fields(CATALOGUE[0])}
    assert "available" not in names
    assert "redeemable" not in names
    assert "availability" not in names


# --- derived behaviour with a live provider ---------------------------


def test_live_provider_gates_on_balance(db_session):
    user = _user(db_session, "sub-live", "Live User")
    _credit(db_session, user, 600)  # covers airtime (500), not data (1000)

    view = build_catalogue(db_session, user_id=user.id, provider_mode="live")
    assert view.provider_connected is True

    by_key = {r.item.key: r for r in view.rows}
    assert by_key["airtime"].availability is Availability.REDEEMABLE
    assert by_key["airtime"].shortfall_cents == 0
    assert by_key["data"].availability is Availability.INSUFFICIENT_CREDIT
    assert by_key["data"].shortfall_cents == 400
    assert by_key["cash_out"].shortfall_cents == 1400


def test_shortfall_never_goes_negative(db_session):
    user = _user(db_session, "sub-rich", "Rich User")
    _credit(db_session, user, 99_999)
    view = build_catalogue(db_session, user_id=user.id, provider_mode="live")
    assert all(r.shortfall_cents >= 0 for r in view.rows)
    assert all(r.shortfall_cents == 0 for r in view.rows)


def test_zero_balance_is_an_honest_zero(db_session):
    user = _user(db_session, "sub-zero", "New User")
    view = build_catalogue(db_session, user_id=user.id, provider_mode="live")
    assert view.balance_cents == 0
    assert view.any_redeemable is False
    assert all(
        r.availability is Availability.INSUFFICIENT_CREDIT for r in view.rows
    )
    # The shortfall must equal the full threshold, not a discounted one.
    assert {r.shortfall_cents for r in view.rows} == {
        i.threshold_cents for i in CATALOGUE
    }


def test_balance_reads_the_reward_ledger_not_a_stored_field(db_session):
    user = _user(db_session, "sub-ledger", "Ledger User")
    assert build_catalogue(db_session, user_id=user.id, provider_mode="live").balance_cents == 0
    _credit(db_session, user, 200, seq=1)
    _credit(db_session, user, 200, seq=2)
    assert (
        build_catalogue(db_session, user_id=user.id, provider_mode="live").balance_cents
        == 400
    )


def test_availability_for_is_pure_and_total():
    """Every combination resolves to exactly one documented state."""
    item = CATALOGUE[0]
    assert (
        availability_for(item, balance_cents=0, provider_connected=False)
        is Availability.PROVIDER_NOT_CONNECTED
    )
    assert (
        availability_for(item, balance_cents=10**9, provider_connected=False)
        is Availability.PROVIDER_NOT_CONNECTED
    )
    assert (
        availability_for(item, balance_cents=0, provider_connected=True)
        is Availability.INSUFFICIENT_CREDIT
    )
    assert (
        availability_for(
            item, balance_cents=item.threshold_cents, provider_connected=True
        )
        is Availability.REDEEMABLE
    )


# --- redemption: the payment leg that was missing ---------------------


class _RecordingProvider:
    """Stands in for DemoProvider, and records what it was asked to do."""

    def __init__(self, mode="live"):
        self.mode = mode
        self.calls = []

    def submit(self, user_ref, amount_cents, idempotency_key):
        from app.provider import PaymentAttempt as ProviderAttempt, PaymentState
        from datetime import datetime, timezone

        self.calls.append((user_ref, amount_cents, idempotency_key))
        return ProviderAttempt(
            id=f"prov-{len(self.calls)}",
            user_ref=user_ref,
            amount_cents=amount_cents,
            provider_mode=self.mode,
            provider_reference=f"ref-{len(self.calls)}",
            state=PaymentState.SUBMITTED,
            requested_at=datetime.now(timezone.utc),
        )


def test_redeem_creates_a_payment_attempt_and_calls_the_provider(db_session):
    """The leg that did not exist before: credit -> provider call."""
    from app.models import PaymentAttempt
    from app.rewards import redeem
    from sqlalchemy import select

    user = _user(db_session, "sub-redeem", "Redeemer")
    _credit(db_session, user, 5000)
    provider = _RecordingProvider()

    attempt = redeem(
        db_session,
        user_id=user.id,
        key="airtime",
        provider_mode="live",
        provider=provider,
        idempotency_key="redeem-1",
    )

    assert provider.calls == [(str(user.id), 500, "redeem-1")]
    assert attempt.provider_reference == "ref-1"
    rows = db_session.execute(select(PaymentAttempt)).scalars().all()
    assert len(rows) == 1
    assert rows[0].amount_cents == 500


def test_redeem_is_idempotent_on_the_key(db_session):
    """A double-tapped Redeem reserves once and pays once."""
    from app.models import PaymentAttempt
    from app.rewards import redeem
    from sqlalchemy import select

    user = _user(db_session, "sub-idem", "Double Tapper")
    _credit(db_session, user, 5000)
    provider = _RecordingProvider()

    first = redeem(db_session, user_id=user.id, key="airtime",
                   provider_mode="live", provider=provider, idempotency_key="same")
    second = redeem(db_session, user_id=user.id, key="airtime",
                    provider_mode="live", provider=provider, idempotency_key="same")

    assert first.id == second.id
    assert len(provider.calls) == 1, "provider must not be called twice"
    assert len(db_session.execute(select(PaymentAttempt)).scalars().all()) == 1


def test_demo_provider_redemption_is_refused_at_the_service_layer(db_session):
    """Not just hidden in the UI -- the service refuses it outright."""
    from app.rewards import RedemptionRefused, redeem

    user = _user(db_session, "sub-demo-redeem", "Demo User")
    _credit(db_session, user, 100_000)
    provider = _RecordingProvider(mode="demo")

    with pytest.raises(RedemptionRefused) as exc:
        redeem(db_session, user_id=user.id, key="airtime",
               provider_mode="demo", provider=provider, idempotency_key="d1")
    assert exc.value.code == "PROVIDER_NOT_CONNECTED"
    assert provider.calls == [], "the provider must never be called in demo mode"


def test_redeem_refuses_beyond_the_ledger_balance(db_session):
    from app.rewards import RedemptionRefused, redeem

    user = _user(db_session, "sub-poor", "Low Balance")
    _credit(db_session, user, 100)  # below the R5 airtime threshold
    provider = _RecordingProvider()

    with pytest.raises(RedemptionRefused) as exc:
        redeem(db_session, user_id=user.id, key="airtime",
               provider_mode="live", provider=provider, idempotency_key="p1")
    assert exc.value.code == "INSUFFICIENT_CREDIT"
    assert provider.calls == []


def test_redeem_refuses_an_unknown_reward(db_session):
    from app.rewards import RedemptionRefused, redeem

    user = _user(db_session, "sub-unknown", "Curious")
    _credit(db_session, user, 100_000)
    provider = _RecordingProvider()

    with pytest.raises(RedemptionRefused) as exc:
        redeem(db_session, user_id=user.id, key="free_iphone",
               provider_mode="live", provider=provider, idempotency_key="u1")
    assert exc.value.code == "UNKNOWN_REWARD"
    assert provider.calls == []
