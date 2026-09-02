"""Reward catalogue — what a contributor's credit can actually become.

This module exists to answer one question honestly: the ledger says a
speaker is owed money, so what can they do with it?

Three rules shape everything here, and each is enforced structurally
rather than by convention:

1. **No invented merchants.** The reference design this screen follows
   lists retailer discounts and a phone giveaway. AMAZWI has no retail
   partners and no prize draw, and inventing either would put a fake
   commercial relationship in front of a judge. Every catalogue item is
   a product MTN MoMo genuinely operates -- airtime, data, wallet
   cash-out -- and nothing else.

2. **Redeemability is derived, never stored.** `CatalogueItem` has no
   "available" field to set wrongly. Availability is computed from the
   live provider mode every time the catalogue is built, so a demo
   provider structurally cannot present a redeemable item.

3. **One currency.** The ledger is denominated in rand cents, so this
   screen is too. Inventing a parallel "points" balance would create a
   second source of truth for money, which is the one thing
   05_BUILD.md's money rules are there to prevent.

CROSS-LANE, PENDING SBU'S REVIEW: what a contributor may redeem credit
for, and at what threshold, is a money decision. The thresholds below
are placeholders chosen to be obviously round rather than researched,
and they are labelled as proposed in the API response.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum

from sqlalchemy.orm import Session

from app.arcade import earned_cents


class Availability(str, Enum):
    """Why an item can or cannot be redeemed right now."""

    REDEEMABLE = "REDEEMABLE"
    """Provider is live and the balance covers the threshold."""

    INSUFFICIENT_CREDIT = "INSUFFICIENT_CREDIT"
    """Provider is live, but the contributor has not earned enough yet."""

    PROVIDER_NOT_CONNECTED = "PROVIDER_NOT_CONNECTED"
    """No live MoMo provider. Nothing here can be redeemed, and the UI
    must say so rather than showing a button that cannot work."""


@dataclass(frozen=True)
class CatalogueItem:
    """One thing credit can become.

    Deliberately has no `available` boolean -- see `build_catalogue`.
    """

    key: str
    title: str
    description: str
    threshold_cents: int
    momo_product: str
    """The real MTN MoMo product this maps to. Not a partner brand."""


# Only products MTN MoMo actually operates. Adding a retailer or a prize
# draw here requires a real, signed relationship -- not a design mock.
CATALOGUE: tuple[CatalogueItem, ...] = (
    CatalogueItem(
        key="airtime",
        title="Airtime top-up",
        description="Send airtime to your own registered number.",
        threshold_cents=500,
        momo_product="Airtime purchase",
    ),
    CatalogueItem(
        key="data",
        title="Data bundle",
        description="Turn what you earned into data for your phone.",
        threshold_cents=1000,
        momo_product="Data bundle purchase",
    ),
    CatalogueItem(
        key="cash_out",
        title="Cash out to your MoMo wallet",
        description="Move your credit into the wallet you already use.",
        threshold_cents=2000,
        momo_product="Wallet transfer",
    ),
)


@dataclass(frozen=True)
class CatalogueRow:
    item: CatalogueItem
    availability: Availability
    shortfall_cents: int
    """How much more is needed. 0 when the threshold is already met."""


@dataclass(frozen=True)
class RewardsView:
    balance_cents: int
    provider_mode: str
    provider_connected: bool
    rows: tuple[CatalogueRow, ...]

    @property
    def any_redeemable(self) -> bool:
        return any(r.availability is Availability.REDEEMABLE for r in self.rows)


def is_live_provider(provider_mode: str) -> bool:
    """Only an explicitly live provider counts as connected.

    Written as an allowlist rather than `!= "demo"`: a new mode added
    later (sandbox, staging, mock) must be opted in deliberately, not
    treated as live because nobody remembered to exclude it.
    """
    return provider_mode.strip().lower() in {"live", "production"}


def availability_for(
    item: CatalogueItem, *, balance_cents: int, provider_connected: bool
) -> Availability:
    if not provider_connected:
        return Availability.PROVIDER_NOT_CONNECTED
    if balance_cents < item.threshold_cents:
        return Availability.INSUFFICIENT_CREDIT
    return Availability.REDEEMABLE


def build_catalogue(
    session: Session, *, user_id: uuid.UUID, provider_mode: str
) -> RewardsView:
    """Build the catalogue for one contributor against the live provider.

    `balance_cents` reads `reward_events` -- the ledger of record. It is
    money CREDITED, never money paid out, and no caller may describe it
    as a wallet balance.
    """
    balance = earned_cents(session, user_id)
    connected = is_live_provider(provider_mode)

    rows = tuple(
        CatalogueRow(
            item=item,
            availability=availability_for(
                item, balance_cents=balance, provider_connected=connected
            ),
            shortfall_cents=max(0, item.threshold_cents - balance),
        )
        for item in CATALOGUE
    )
    return RewardsView(
        balance_cents=balance,
        provider_mode=provider_mode,
        provider_connected=connected,
        rows=rows,
    )
