"""Economical MoMo smoke check.

Default behaviour only obtains collection/disbursement OAuth tokens. A paid
sandbox transfer requires both --confirm-test-transfer and the environment
guard MOMO_ENABLE_TEST_TRANSFERS=true (default ceiling is one cent).
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys

if __package__ in {None, ""}:
    # Support the documented `python scripts/momo_smoke.py` invocation when
    # the current working directory is starter/backend.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.momo import MomoApiError, MomoClient, MomoConfig, MomoConfigurationError


def load_local_env() -> None:
    path = Path(__file__).resolve().parents[1] / ".env"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--confirm-test-transfer", action="store_true")
    args = parser.parse_args()
    load_local_env()
    try:
        config = MomoConfig.from_env()
    except MomoConfigurationError as exc:
        print(f"configuration error: {exc}")
        return 2
    client = MomoClient(config)
    try:
        try:
            client._token("collection")
            client._token("disbursement")
        except MomoApiError as exc:
            print(f"MoMo smoke failed: {exc}")
            return 1
        print("MoMo OAuth: collection and disbursement tokens obtained (values withheld).")
        if not args.confirm_test_transfer:
            print("No transfer sent. Use --confirm-test-transfer only for an approved sandbox test.")
            return 0
        if not config.test_payee_msisdn or not config.test_currency:
            print("transfer blocked: MOMO_TEST_PAYEE_MSISDN and MOMO_TEST_CURRENCY are required")
            return 2
        reference = client.transfer(
            amount_cents=1,
            payee_msisdn=config.test_payee_msisdn,
            currency=config.test_currency,
            external_id="amazwi-sandbox-smoke",
        )
        print(f"Sandbox transfer accepted (reference withheld): {reference[:8]}…")
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())
