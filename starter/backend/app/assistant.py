"""Guarded, deterministic assistant intent handling.

The assistant is deliberately useful before any model is configured. It can
navigate existing product surfaces and explain the ledger boundary, but it
cannot execute payments, change verification truth, or choose arbitrary URLs.
Model-backed classification can be added behind this same response contract.
"""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class AssistantResponse:
    reply: str
    intent: str
    route: str | None
    provider: str
    advisory: bool = True


_ROUTES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("/rewards", ("reward", "rewards", "wallet", "credit")),
    ("/impact", ("impact", "map", "coverage", "language gap")),
    ("/consent", ("consent", "permission", "privacy")),
    ("/record", ("record", "recording", "speak", "contribute")),
    ("/verify", ("verify", "verification", "listen to a contribution")),
    ("/ops", ("operator", "language ops", "mission")),
    ("/dashboard", ("dashboard", "progress", "leaderboard", "arcade")),
    ("/", ("home", "start", "play", "game")),
)


def _normalise(message: str) -> str:
    return re.sub(r"\s+", " ", message.strip().lower())


def _contains_any(message: str, terms: tuple[str, ...]) -> bool:
    return any(term in message for term in terms)


def _reply(language: str, english: str, zulu: str, setswana: str) -> str:
    if language == "zu":
        return zulu
    if language == "tn":
        return setswana
    return english


def handle_assistant_message(message: str, language: str = "en") -> AssistantResponse:
    """Return one safe, allowlisted intent for a user message."""
    text = _normalise(message)
    if not text:
        return AssistantResponse(
            "Tell me whether you want to play, record, verify, view rewards, or see impact.",
            "HELP",
            None,
            "deterministic",
        )

    if _contains_any(text, ("cash out", "cashout", "cash me out", "pay me", "send money", "transfer money", "redeem")):
        return AssistantResponse(
            _reply(
                language,
                "I cannot move money from chat. I can show your credited reward, then a separate confirmed cash-out flow can handle settlement.",
                "Angikwazi ukuhambisa imali kule ngxoxo. Ngingakubonisa umvuzo ofakiwe, bese inqubo eqinisekisiwe yokukhokha iphatha i-settlement.",
                "Ga ke kgone go tsamaisa madi mo puisanong. Nka go bontsha tuelo e e tsentsweng, mme tsela e e netefaditsweng e tshwara settlement.",
            ),
            "PAYMENT_CONFIRMATION_REQUIRED",
            None,
            "deterministic",
        )

    if _contains_any(text, ("why did i earn", "why was i rewarded", "explain my receipt", "receipt", "credited")):
        return AssistantResponse(
            _reply(
                language,
                "Two human listeners understood your clue, so the deterministic ledger credited your reward. That credit is not the same as provider settlement.",
                "Abalaleli ababili bayiqondile inkomba yakho, ngakho i-ledger efanele ifake umvuzo wakho. Lokho kufakwa akufani ne-settlement yomnikezeli.",
                "Bareetsi ba le babedi ba tlhalogantse lesedi la gago, ka jalo ledger e e tlhomameng e tsentse tuelo. Seo ga se tshwane le settlement ya mofani.",
            ),
            "EXPLAIN_RECEIPT",
            "/rewards",
            "deterministic",
        )

    for route, terms in _ROUTES:
        if _contains_any(text, terms):
            return AssistantResponse(
                _reply(
                    language,
                    f"I can take you to {route}. The app will ask for any permission or confirmation required there.",
                    f"Ngingakuyisa ku-{route}. Uhlelo lokusebenza luzocela imvume noma ukuqinisekisa lapho kudingeka khona.",
                    f"Nka go isa kwa {route}. App e tla kopa tetla kgotsa netefatso fa go tlhokega.",
                ),
                "NAVIGATE",
                route,
                "deterministic",
            )

    return AssistantResponse(
        _reply(
            language,
            "I can help you play, record, verify, view rewards, check impact, or open Language Ops.",
            "Ngingakusiza udlale, uqophe, uqinisekise, ubone imivuzo, uhlole umthelela, noma uvule i-Language Ops.",
            "Nka go thusa go tshameka, go rekota, go netefatsa, go bona dituelo, go bona impact, kgotsa go bula Language Ops.",
        ),
        "HELP",
        None,
        "deterministic",
    )
