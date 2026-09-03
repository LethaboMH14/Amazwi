"""Structural guard on the direction money moves.

MTN MoMo has two separate products and they move money in opposite
directions:

- **Collections** (`request_to_pay`) takes money **IN** from a payer.
- **Disbursement** (`transfer`) pays money **OUT** to a payee.

Wiring Collections into the contributor payout path would *charge the
person you meant to pay*. That mistake is about five minutes of work and
reads almost identically at the call site, which is exactly why it needs
a test rather than a comment.

Collections legitimately belongs where a sponsor funds a mission. It does
not belong anywhere in the redemption or reward-payout path.

Flagged by Lethabo in `HANDOVER_SBU.md` (03 Sep PING). The code was
already correct when this test was written; nothing was enforcing that it
stayed correct.
"""
from __future__ import annotations

from pathlib import Path
import re

APP_ROOT = Path(__file__).resolve().parents[1] / "app"

# The only module allowed to name `request_to_pay` is the client that
# defines it. Sponsor-funding code may be added later, but it must be
# added deliberately: extend this list in the same commit, so the money
# direction gets re-reviewed rather than silently widened.
_COLLECTIONS_CALLERS_ALLOWED = {"momo.py"}

# Modules on the contributor payout path. If any of these ever names
# `request_to_pay`, money is about to move the wrong way.
_PAYOUT_PATH = ("rewards.py", "ledger.py", "momo_provider.py", "providers.py")


def test_collections_is_not_reachable_from_any_payout_module():
    """`request_to_pay` must not appear on the money-OUT path."""
    offenders = []
    for name in _PAYOUT_PATH:
        path = APP_ROOT / name
        if not path.exists():
            continue
        if re.search(r"\brequest_to_pay\b", path.read_text(encoding="utf-8")):
            offenders.append(name)
    assert offenders == [], (
        f"{offenders} reference request_to_pay (MoMo Collections, money IN). "
        "The payout path must use MomoClient.transfer (Disbursement, money OUT); "
        "Collections here would charge the contributor instead of paying them."
    )


def test_only_the_momo_client_names_request_to_pay():
    """Nothing in app/ calls Collections yet, and adding a caller is deliberate."""
    callers = set()
    for path in APP_ROOT.rglob("*.py"):
        if re.search(r"\brequest_to_pay\b", path.read_text(encoding="utf-8")):
            callers.add(path.relative_to(APP_ROOT).as_posix())
    unexpected = callers - _COLLECTIONS_CALLERS_ALLOWED
    assert unexpected == set(), (
        f"{sorted(unexpected)} now reference MoMo Collections. If this is the "
        "sponsor mission-funding path, add it to _COLLECTIONS_CALLERS_ALLOWED "
        "in the same commit so the money direction is reviewed, not assumed."
    )


def test_the_payout_provider_uses_disbursement():
    """The positive half: the payout adapter really does call transfer()."""
    text = (APP_ROOT / "momo_provider.py").read_text(encoding="utf-8")
    assert re.search(r"\bself\._client\.transfer\(", text), (
        "momo_provider.submit must pay out via MomoClient.transfer (Disbursement). "
        "If this assertion fails, check what it is calling instead."
    )
