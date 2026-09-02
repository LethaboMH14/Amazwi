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

from app.provider import DemoProvider, PaymentProvider

# The process-wide provider. `DemoProvider` is deliberate: swapping in a
# live adapter is a money and deployment decision (05_BUILD.md section 2),
# not something a route should be able to do implicitly.
provider: PaymentProvider = DemoProvider()


def get_provider() -> PaymentProvider:
    """FastAPI-dependency-friendly accessor, and a seam for tests."""
    return provider
