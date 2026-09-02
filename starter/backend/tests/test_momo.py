from __future__ import annotations

import base64
import json
from uuid import UUID

import httpx
import pytest

from app.momo import MomoApiError, MomoClient, MomoConfig, MomoConfigurationError


def config(**overrides) -> MomoConfig:
    values = dict(
        base_url="https://sandbox.example",
        target_environment="sandbox",
        api_user="api-user",
        api_key="api-key",
        collection_subscription_key="collection-sub",
        disbursement_subscription_key="disbursement-sub",
        enable_test_transfers=True,
        max_test_cents=1,
    )
    values.update(overrides)
    return MomoConfig(**values)


def test_token_is_cached_and_credentials_are_not_sent_in_request_body():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        assert request.url.path == "/collection/token/"
        assert request.content == b"grant_type=client_credentials"
        auth = request.headers["Authorization"]
        expected = base64.b64encode(b"api-user:api-key").decode()
        assert auth == f"Basic {expected}"
        return httpx.Response(200, json={"access_token": "token", "expires_in": 3600})

    client = MomoClient(config(), client=httpx.Client(transport=httpx.MockTransport(handler)))
    assert client._token("collection") == "token"
    assert client._token("collection") == "token"
    assert len(calls) == 1


def test_transfer_requires_explicit_enable_flag():
    client = MomoClient(config(enable_test_transfers=False), client=httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(500))))
    with pytest.raises(MomoConfigurationError, match="disabled"):
        client.transfer(
            amount_cents=1,
            payee_msisdn="27820000000",
            currency="EUR",
            external_id="demo-1",
        )


def test_transfer_is_capped_and_uses_disbursement_subscription():
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path == "/disbursement/token/":
            return httpx.Response(200, json={"access_token": "token", "expires_in": 3600})
        assert request.url.path == "/disbursement/v1_0/transfer"
        assert request.headers["Ocp-Apim-Subscription-Key"] == "disbursement-sub"
        assert request.headers["X-Target-Environment"] == "sandbox"
        assert UUID(request.headers["X-Reference-Id"])
        body = json.loads(request.content)
        assert body["amount"] == "0.01"
        assert body["currency"] == "EUR"
        assert body["payee"]["partyId"] == "27820000000"
        return httpx.Response(202)

    client = MomoClient(config(), client=httpx.Client(transport=httpx.MockTransport(handler)))
    reference = client.transfer(
        amount_cents=1,
        payee_msisdn="27820000000",
        currency="EUR",
        external_id="demo-1",
    )
    assert UUID(reference)
    with pytest.raises(MomoConfigurationError, match="exceeds"):
        client.transfer(
            amount_cents=2,
            payee_msisdn="27820000000",
            currency="EUR",
            external_id="demo-2",
        )
    assert len(requests) == 2


def test_request_to_pay_returns_reference_only_after_202():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/collection/token/":
            return httpx.Response(200, json={"access_token": "token", "expires_in": 3600})
        assert request.url.path == "/collection/v1_0/requesttopay"
        return httpx.Response(202)

    client = MomoClient(config(), client=httpx.Client(transport=httpx.MockTransport(handler)))
    reference = client.request_to_pay(
        amount_cents=1,
        payer_msisdn="27820000000",
        currency="EUR",
        external_id="demo-collection-1",
    )
    assert UUID(reference)


def test_api_error_is_sanitised():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="secret provider response")

    client = MomoClient(config(), client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(MomoApiError, match="HTTP 401") as error:
        client._token("collection")
    assert "secret provider response" not in str(error.value)
