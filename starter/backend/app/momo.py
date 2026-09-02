"""Small, defensive MTN MoMo Open API client.

The demo provider remains the default.  This module is deliberately opt-in:
it can obtain a sandbox token without moving money, while payment/transfer
calls require an explicit sandbox flag and a very small configured ceiling.
No credential or response body is written to logs.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import os
from typing import Any
from uuid import UUID, uuid4

import httpx


class MomoConfigurationError(RuntimeError):
    """The local MoMo environment is incomplete or unsafe."""


class MomoApiError(RuntimeError):
    """A MoMo call failed; the message intentionally excludes response data."""


@dataclass(frozen=True)
class MomoConfig:
    base_url: str
    target_environment: str
    api_user: str
    api_key: str
    collection_subscription_key: str
    disbursement_subscription_key: str
    test_currency: str | None = None
    test_payer_msisdn: str | None = None
    test_payee_msisdn: str | None = None
    callback_url: str | None = None
    enable_test_transfers: bool = False
    max_test_cents: int = 1

    @classmethod
    def from_env(cls) -> "MomoConfig":
        def required(name: str) -> str:
            value = (os.environ.get(name) or "").strip()
            if not value:
                raise MomoConfigurationError(f"{name} is required")
            return value

        raw_max = (os.environ.get("MOMO_MAX_TEST_CENTS") or "1").strip()
        try:
            max_test_cents = int(raw_max)
        except ValueError as exc:
            raise MomoConfigurationError("MOMO_MAX_TEST_CENTS must be an integer") from exc
        if max_test_cents < 1:
            raise MomoConfigurationError("MOMO_MAX_TEST_CENTS must be at least 1")

        target = (os.environ.get("MOMO_TARGET_ENVIRONMENT") or "sandbox").strip()
        if target.lower() == "production":
            raise MomoConfigurationError("production MoMo is disabled for this build")
        return cls(
            base_url=required("MOMO_BASE_URL").rstrip("/"),
            target_environment=target,
            api_user=required("MOMO_API_USER"),
            api_key=required("MOMO_API_KEY"),
            collection_subscription_key=required("MOMO_COLLECTION_SUBSCRIPTION_KEY"),
            disbursement_subscription_key=required("MOMO_DISBURSEMENT_SUBSCRIPTION_KEY"),
            test_currency=(os.environ.get("MOMO_TEST_CURRENCY") or "").strip() or None,
            test_payer_msisdn=(os.environ.get("MOMO_TEST_PAYER_MSISDN") or "").strip() or None,
            test_payee_msisdn=(os.environ.get("MOMO_TEST_PAYEE_MSISDN") or "").strip() or None,
            callback_url=(os.environ.get("MOMO_CALLBACK_URL") or "").strip() or None,
            enable_test_transfers=(os.environ.get("MOMO_ENABLE_TEST_TRANSFERS") or "").lower() == "true",
            max_test_cents=max_test_cents,
        )


class MomoClient:
    """Collection and disbursement calls with token caching and hard guards."""

    def __init__(self, config: MomoConfig, *, client: httpx.Client | None = None) -> None:
        self.config = config
        self.client = client or httpx.Client(timeout=10.0)
        self._tokens: dict[str, tuple[str, datetime]] = {}
        self._references: dict[str, tuple[str, str]] = {}

    def close(self) -> None:
        self.client.close()

    def _token(self, product: str) -> str:
        cached = self._tokens.get(product)
        now = datetime.now(timezone.utc)
        if cached and cached[1] > now + timedelta(seconds=30):
            return cached[0]
        if product not in {"collection", "disbursement"}:
            raise MomoConfigurationError("unknown MoMo product")
        response = self.client.post(
            f"{self.config.base_url}/{product}/token/",
            auth=(self.config.api_user, self.config.api_key),
            headers={"Ocp-Apim-Subscription-Key": getattr(self.config, f"{product}_subscription_key")},
            data={"grant_type": "client_credentials"},
        )
        if response.status_code >= 400:
            raise MomoApiError(f"MoMo {product} token failed (HTTP {response.status_code})")
        try:
            payload = response.json()
            token = str(payload["access_token"])
            expires = int(payload.get("expires_in", 3600))
        except (ValueError, KeyError, TypeError) as exc:
            raise MomoApiError("MoMo token response was invalid") from exc
        self._tokens[product] = (token, now + timedelta(seconds=max(60, expires)))
        return token

    def _headers(self, product: str, reference: str, token: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Ocp-Apim-Subscription-Key": getattr(self.config, f"{product}_subscription_key"),
            "X-Target-Environment": self.config.target_environment,
            "X-Reference-Id": reference,
            "Content-Type": "application/json",
        }

    def _guard_amount(self, amount_cents: int) -> None:
        if amount_cents < 1:
            raise MomoConfigurationError("amount must be at least one cent")
        if amount_cents > self.config.max_test_cents:
            raise MomoConfigurationError(
                f"amount exceeds MOMO_MAX_TEST_CENTS ({self.config.max_test_cents})"
            )
        if not self.config.enable_test_transfers:
            raise MomoConfigurationError(
                "test transfer disabled; set MOMO_ENABLE_TEST_TRANSFERS=true explicitly"
            )
        if self.config.target_environment.lower() == "production":
            raise MomoConfigurationError("production transfers are disabled")

    @staticmethod
    def _amount(amount_cents: int) -> str:
        return f"{amount_cents / 100:.2f}"

    def request_to_pay(
        self,
        *,
        amount_cents: int,
        payer_msisdn: str,
        currency: str,
        external_id: str,
        reference_id: UUID | None = None,
        payer_message: str = "AMAZWI sandbox test",
        payee_note: str = "AMAZWI sandbox test",
        transfer_type: str = "CUSTOM_PAYMENT",
    ) -> str:
        self._guard_amount(amount_cents)
        reference = str(reference_id or uuid4())
        body: dict[str, Any] = {
            "amount": self._amount(amount_cents),
            "currency": currency,
            "externalId": external_id,
            "payer": {"partyIdType": "MSISDN", "partyId": payer_msisdn},
            "payerMessage": payer_message,
            "payeeNote": payee_note,
            "transferType": transfer_type,
        }
        if self.config.callback_url:
            body["callbackUrl"] = self.config.callback_url
        response = self.client.post(
            f"{self.config.base_url}/collection/v1_0/requesttopay",
            headers=self._headers("collection", reference, self._token("collection")),
            json=body,
        )
        if response.status_code != 202:
            raise MomoApiError(f"MoMo request-to-pay failed (HTTP {response.status_code})")
        self._references[reference] = ("collection", "/collection/v1_0/requesttopay")
        return reference

    def transfer(
        self,
        *,
        amount_cents: int,
        payee_msisdn: str,
        currency: str,
        external_id: str,
        reference_id: UUID | None = None,
        payer_message: str = "AMAZWI sandbox reward",
        payee_note: str = "AMAZWI sandbox reward",
        transfer_type: str = "CUSTOM_PAYMENT",
    ) -> str:
        self._guard_amount(amount_cents)
        reference = str(reference_id or uuid4())
        body: dict[str, Any] = {
            "amount": self._amount(amount_cents),
            "currency": currency,
            "externalId": external_id,
            "payee": {"partyIdType": "MSISDN", "partyId": payee_msisdn},
            "payerMessage": payer_message,
            "payeeNote": payee_note,
            "transferType": transfer_type,
        }
        if self.config.callback_url:
            body["callbackUrl"] = self.config.callback_url
        response = self.client.post(
            f"{self.config.base_url}/disbursement/v1_0/transfer",
            headers=self._headers("disbursement", reference, self._token("disbursement")),
            json=body,
        )
        if response.status_code != 202:
            raise MomoApiError(f"MoMo transfer failed (HTTP {response.status_code})")
        self._references[reference] = ("disbursement", "/disbursement/v1_0/transfer")
        return reference

    def status(self, *, product: str, reference_id: str) -> dict[str, Any]:
        """Poll a transaction; callers must reconcile the result idempotently."""
        if product not in {"collection", "disbursement"}:
            raise MomoConfigurationError("unknown MoMo product")
        response = self.client.get(
            f"{self.config.base_url}/{product}/v1_0/{'requesttopay' if product == 'collection' else 'transfer'}/{reference_id}",
            headers=self._headers(product, reference_id, self._token(product)),
        )
        if response.status_code >= 400:
            raise MomoApiError(f"MoMo {product} status failed (HTTP {response.status_code})")
        payload = response.json()
        return payload if isinstance(payload, dict) else {"status": payload}
