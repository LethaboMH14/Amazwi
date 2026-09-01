"""Payment-provider adapter interface. No product concept here — generic reward/payout shape only."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol
from uuid import uuid4


class PaymentState(str, Enum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"


@dataclass
class PaymentAttempt:
    id: str
    user_ref: str
    amount_cents: int
    provider_mode: str
    provider_reference: str | None
    state: PaymentState
    requested_at: datetime
    resolved_at: datetime | None = None


class PaymentProvider(Protocol):
    mode: str

    def submit(self, user_ref: str, amount_cents: int, idempotency_key: str) -> PaymentAttempt: ...

    def get_status(self, attempt_id: str) -> PaymentAttempt: ...


class DemoProvider:
    """In-memory provider. Always labelled, never presented as real settlement."""

    mode = "demo"

    def __init__(self) -> None:
        self._attempts: dict[str, PaymentAttempt] = {}
        self._idempotency: dict[str, str] = {}

    def submit(self, user_ref: str, amount_cents: int, idempotency_key: str) -> PaymentAttempt:
        existing_id = self._idempotency.get(idempotency_key)
        if existing_id:
            return self._attempts[existing_id]

        attempt = PaymentAttempt(
            id=str(uuid4()),
            user_ref=user_ref,
            amount_cents=amount_cents,
            provider_mode=self.mode,
            provider_reference=f"demo-{uuid4().hex[:8]}",
            state=PaymentState.SUBMITTED,
            requested_at=datetime.now(timezone.utc),
        )
        self._attempts[attempt.id] = attempt
        self._idempotency[idempotency_key] = attempt.id
        return attempt

    def get_status(self, attempt_id: str) -> PaymentAttempt:
        attempt = self._attempts[attempt_id]
        if attempt.state == PaymentState.SUBMITTED:
            attempt.state = PaymentState.PAID
            attempt.resolved_at = datetime.now(timezone.utc)
        return attempt
