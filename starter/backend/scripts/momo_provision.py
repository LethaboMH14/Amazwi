"""Provision and verify MoMo sandbox credentials, for BOTH products.

Why this exists
---------------
On 3 Sep 2026 the stored credentials stopped working. The failure looked
like a code bug (HTTP 401 on the token call) but was not: MTN answered

    401 "Access denied due to invalid subscription key.
         Make sure to provide a valid key for an active subscription."

and it answered *identically* for a key of 32 zeros. That comparison is
the whole diagnosis -- a real key and an obviously fake one being treated
the same means the gateway never recognised ours, so nothing downstream
(api user, api key, token body, target environment) can be the cause.

A subscription key can only be issued from the MTN Developer Portal by a
human with the account. This script does everything that comes AFTER
that, so pasting a fresh key is the only manual step:

    1. verify the subscription key is actually active
    2. create an API user  (POST /v1_0/apiuser)
    3. create its API key  (POST /v1_0/apiuser/{id}/apikey)
    4. prove a real token can be obtained

Run it per product. Collections is money IN (a sponsor funding a
campaign). Disbursement is money OUT (paying a contributor). They are
separate MTN subscriptions with separate keys, and AMAZWI needs
Disbursement for any speaker payout.

    python scripts/momo_provision.py --product collection
    python scripts/momo_provision.py --product disbursement

Secrets are never printed in full: the API key is shown masked, and
--write appends it to the env file rather than the terminal.
"""
from __future__ import annotations

import argparse
import os
import sys
import uuid
from pathlib import Path

import httpx

BACKEND = Path(__file__).resolve().parents[1]
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

# Credentials live in the REPO ROOT .env, not starter/backend/.env. The
# smoke script only looked in the latter, so it reported "MOMO_BASE_URL is
# required" while a fully populated .env sat two directories up.
ENV_CANDIDATES = [
    BACKEND / ".env",
    BACKEND.parents[1] / ".env",
]


def load_env() -> Path | None:
    """Load the first env file found, and report which one was used."""
    for path in ENV_CANDIDATES:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
        return path
    return None


def mask(secret: str) -> str:
    return f"{len(secret)} chars, ends …{secret[-4:]}" if len(secret) > 4 else "(short)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--product", choices=["collection", "disbursement"], required=True)
    parser.add_argument(
        "--write",
        action="store_true",
        help="append the new credentials to the env file instead of printing them",
    )
    args = parser.parse_args()

    env_path = load_env()
    print(f"env file: {env_path or 'none found'}")

    base = (os.environ.get("MOMO_BASE_URL") or "https://sandbox.momodeveloper.mtn.com").rstrip("/")
    target = (os.environ.get("MOMO_TARGET_ENVIRONMENT") or "sandbox").strip()
    if target.lower() == "production":
        print("refusing: production provisioning is not done by this script")
        return 2

    key_var = f"MOMO_{args.product.upper()}_SUBSCRIPTION_KEY"
    sub_key = (os.environ.get(key_var) or "").strip()
    if not sub_key:
        print(f"{key_var} is not set. Get it from the MTN Developer Portal:")
        print("  https://momodeveloper.mtn.com/ -> Products -> subscribe -> Primary key")
        return 2

    callback = (os.environ.get("MOMO_CALLBACK_URL") or "https://example.com/momo").strip()
    host = callback.split("://", 1)[-1].split("/", 1)[0]

    with httpx.Client(timeout=30) as client:
        # 1. Is the subscription key active at all? Checked FIRST, because
        #    every later failure is unreadable if it is not.
        probe = client.get(
            f"{base}/v1_0/apiuser/{uuid.uuid4()}",
            headers={"Ocp-Apim-Subscription-Key": sub_key},
        )
        if probe.status_code == 401 and "subscription key" in probe.text.lower():
            print(f"\nBLOCKED: {key_var} is not an active subscription.")
            print("  MTN returns the same 401 for this key as for a key of all zeros,")
            print("  so the gateway does not recognise it. This cannot be fixed in code.")
            print("\n  Fix it in the portal, then re-run:")
            print("    1. https://momodeveloper.mtn.com/ -> sign in")
            print(f"    2. Products -> {args.product.title()} -> Subscribe (if not already)")
            print("    3. Profile -> copy the PRIMARY KEY for that subscription")
            print(f"    4. Put it in {env_path} as {key_var}=<key>")
            return 1
        print(f"subscription key: active ({key_var})")

        # 2. Create the API user. The X-Reference-Id we send BECOMES the
        #    api user id -- MTN does not return one.
        api_user = str(uuid.uuid4())
        created = client.post(
            f"{base}/v1_0/apiuser",
            headers={
                "X-Reference-Id": api_user,
                "Ocp-Apim-Subscription-Key": sub_key,
                "Content-Type": "application/json",
            },
            json={"providerCallbackHost": host},
        )
        if created.status_code not in (201, 409):
            print(f"apiuser creation failed (HTTP {created.status_code}): {created.text[:160]}")
            return 1
        print(f"api user created: {api_user}")

        # 3. Mint its API key.
        keyed = client.post(
            f"{base}/v1_0/apiuser/{api_user}/apikey",
            headers={"Ocp-Apim-Subscription-Key": sub_key},
        )
        if keyed.status_code not in (200, 201):
            print(f"apikey creation failed (HTTP {keyed.status_code}): {keyed.text[:160]}")
            return 1
        api_key = keyed.json().get("apiKey", "")
        if not api_key:
            print("apikey response contained no apiKey")
            return 1
        print(f"api key minted: {mask(api_key)}")

        # 4. Prove it. No request body -- MTN's WAF returns an HTML
        #    "Request Rejected" page with HTTP 200 if one is sent.
        token = client.post(
            f"{base}/{args.product}/token/",
            auth=(api_user, api_key),
            headers={
                "Ocp-Apim-Subscription-Key": sub_key,
                "X-Target-Environment": target,
            },
        )
        if token.status_code >= 400:
            print(f"token check FAILED (HTTP {token.status_code}): {token.text[:160]}")
            return 1
        print(f"token check: OK ({args.product} token obtained, value withheld)")

    if args.write and env_path:
        # REPLACE in place, never append. The loaders use setdefault, so the
        # FIRST occurrence of a key wins -- appending a fresh credential
        # beneath an existing one leaves the STALE value in force, and the
        # symptom is a freshly minted key appearing not to work at all.
        # (That happened on the first run of this script.)
        existing = env_path.read_text(encoding="utf-8", errors="replace").splitlines()
        updates = {"MOMO_API_USER": api_user, "MOMO_API_KEY": api_key}
        seen = set()
        out = []
        for line in existing:
            name = line.split("=", 1)[0].strip() if "=" in line else ""
            if name in updates:
                if name in seen:
                    continue
                out.append(name + "=" + updates[name])
                seen.add(name)
            else:
                out.append(line)
        for name, value in updates.items():
            if name not in seen:
                out.append(name + "=" + value)
        env_path.write_text("\n".join(out) + "\n", encoding="utf-8")
        print("\nupdated in place: " + str(env_path))
        print("  One api user authenticates against BOTH products (verified),")
        print("  so a single pair serves collection and disbursement.")
    else:
        print("\nAdd these to your env file (or re-run with --write):")
        print(f"  MOMO_API_USER={api_user}")
        print("  MOMO_API_KEY=<the key just minted; re-run with --write to store it>")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
