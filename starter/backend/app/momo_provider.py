"""PaymentProvider backed by the real MTN MoMo Disbursement API.

This is the money-OUT leg. It is deliberately NOT the default: the
process-wide provider in `app/providers.py` stays `DemoProvider` unless
`MOMO_PROVIDER_MODE=MOMO_SANDBOX` is set explicitly.

WHY DISBURSEMENT AND NOT COLLECTIONS -- the trap this file exists to
avoid. MTN issues two products and they move money in opposite
directions:

    Collections   money IN   -- a sponsor funds a campaign
    Disbursement  money OUT  -- a contributor is paid

Redeeming a contributor's ledger credit pays them, so it MUST use
Disbursement. Wiring `requestToPay` (Collections) into the redeem path
would charge the person you meant to pay. Both credentials are present
and both authenticate, so nothing but this comment and the call below
stops that mistake.

WHAT 202 MEANS. `transfer` returns HTTP 202 "accepted for processing".
That is NOT a payment. Verified against the live sandbox on 3 Sep 2026:
a 202-accepted 1-cent transfer reported `status: PENDING` when its
reference was queried a moment later. This adapter therefore reports
`SUBMITTED`, never `PAID`, and only `get_status` may promote it -- and
only when MTN itself says SUCCESSFUL.

Production is refused by `MomoConfig` itself, so this cannot reach real
money regardless of what is configured here.
"""
from __future__ import annotations

import os
from datetime import datetime, timezone

from app.momo import MomoApiError, MomoClient, MomoConfig, MomoConfigurationError
from app.provider import PaymentAttempt, PaymentState


class MomoSandboxProvider:
    """Adapter satisfying the PaymentProvider protocol."""

    mode = "momo_sandbox"

    def __init__(self, client: MomoClient | None = None) -> None:
        self._client = client or MomoClient(MomoConfig.from_env())
        self._by_key: dict[str, PaymentAttempt] = {}

    def close(self) -> None:
        self._client.close()

    def submit(self, user_ref: str, amount_cents: int, idempotency_key: str) -> PaymentAttempt:
        """Send a Disbursement transfer. Idempotent on `idempotency_key`.

        The ledger already refuses to reserve beyond the available
        balance before this is reached, and `MomoClient._guard_amount`
        independently refuses anything above MOMO_MAX_TEST_CENTS. Two
        separate ceilings, deliberately -- one protects the campaign
        budget, the other protects against a coding mistake here.
        """
        existing = self._by_key.get(idempotency_key)
        if existing is not None:
            return existing

        payee = (os.environ.get("MOMO_TEST_PAYEE_MSISDN") or "").strip()
        currency = (os.environ.get("MOMO_TEST_CURRENCY") or "").strip()
        if not payee or not currency:
            raise MomoConfigurationError(
                "MOMO_TEST_PAYEE_MSISDN and MOMO_TEST_CURRENCY are required to disburse"
            )

        now = datetime.now(timezone.utc)
        try:
            reference = self._client.transfer(
                amount_cents=amount_cents,
                payee_msisdn=payee,
                currency=currency,
                external_id=idempotency_key,
            )
        except (MomoApiError, MomoConfigurationError):
            # Surface the failure to the caller as a FAILED attempt rather
            # than an exception: the ledger reservation already exists, and
            # losing it to a traceback would strand the contributor's credit
            # in a reserved-but-unaccounted state.
            attempt = PaymentAttempt(
                id=idempotency_key,
                user_ref=user_ref,
                amount_cents=amount_cents,
                provider_mode=self.mode,
                provider_reference=None,
                state=PaymentState.FAILED,
                requested_at=now,
                resolved_at=now,
            )
            self._by_key[idempotency_key] = attempt
            return attempt

        attempt = PaymentAttempt(
            id=reference,
            user_ref=user_ref,
            amount_cents=amount_cents,
            provider_mode=self.mode,
            provider_reference=reference,
            # SUBMITTED, never PAID. MTN returned 202 "accepted for
            # processing"; the live sandbox reports PENDING immediately
            # afterwards. Only get_status may promote this.
            state=PaymentState.SUBMITTED,
            requested_at=now,
        )
        self._by_key[idempotency_key] = attempt
        return attempt

    def get_status(self, attempt_id: str) -> PaymentAttempt:
        """Ask MTN what actually happened, and report only that."""
        attempt = next(
            (a for a in self._by_key.values() if a.id == attempt_id),
            None,
        )
        if attempt is None:
            raise KeyError(attempt_id)
        if attempt.provider_reference is None:
            return attempt

        try:
            payload = self._client.status(
                product="disbursement", reference_id=attempt.provider_reference
            )
        except MomoApiError:
            return attempt

        # MTN's own vocabulary, mapped conservatively: anything that is not
        # an explicit SUCCESSFUL or FAILED stays SUBMITTED.
        remote = str(payload.get("status", "")).upper()
        if remote == "SUCCESSFUL":
            state = PaymentState.PAID
        elif remote == "FAILED":
            state = PaymentState.FAILED
        else:
            state = PaymentState.SUBMITTED

        updated = PaymentAttempt(
            id=attempt.id,
            user_ref=attempt.user_ref,
            amount_cents=attempt.amount_cents,
            provider_mode=self.mode,
            provider_reference=attempt.provider_reference,
            state=state,
            requested_at=attempt.requested_at,
            resolved_at=datetime.now(timezone.utc)
            if state in (PaymentState.PAID, PaymentState.FAILED)
            else None,
        )
        for key, value in self._by_key.items():
            if value.id == attempt_id:
                self._by_key[key] = updated
                break
        return updated
