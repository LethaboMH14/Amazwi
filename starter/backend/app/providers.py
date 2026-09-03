"""Single owner of the payment-provider instance.

Exists because `routes/arcade.py` previously reached into `app.main`
for the provider, while `app.main` imports that router -- a genuine
import cycle (app.main <-> app.routes.arcade), which `archy cycles`
caught. The local-import-inside-the-function trick made it work at
runtime but left the cycle in the graph, and a cycle stops being
harmless the moment someone adds a second caller.

Both sides now depend on this leaf module instead, so the graph is
acyclic and the provider has one obvious home.
"""
from __future__ import annotations

import os

from app.provider import DemoProvider, PaymentProvider

def _build_provider() -> PaymentProvider:
    """Choose the process-wide provider.

    `DemoProvider` is the default and stays the default. Selecting the
    real MoMo adapter takes an EXPLICIT environment opt-in, because
    swapping it is a money and deployment decision (05_BUILD.md section
    2), not something a route or an import should do implicitly.

    Even when opted in, this is Disbursement against MTN's SANDBOX:
    MomoConfig refuses `production` outright, and MomoClient enforces a
    MOMO_MAX_TEST_CENTS ceiling on every transfer.

    A misconfiguration falls back to the demo provider rather than
    raising at import time -- a backend that will not boot is a worse
    failure than one that is honestly labelled DEMO_PROVIDER, and the
    label is on screen either way.
    """
    if (os.environ.get("MOMO_PROVIDER_MODE") or "").strip().upper() != "MOMO_SANDBOX":
        return DemoProvider()
    try:
        from app.momo_provider import MomoSandboxProvider

        return MomoSandboxProvider()
    except Exception:
        return DemoProvider()


provider: PaymentProvider = _build_provider()


def get_provider() -> PaymentProvider:
    """FastAPI-dependency-friendly accessor, and a seam for tests."""
    return provider
