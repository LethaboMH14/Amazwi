"""OpenAI-compatible LLM client for the advisory Council.

Two providers, one interface. Featherless and AIML both speak the
OpenAI `/chat/completions` shape, so switching between them is a config
change, never a code change.

WHAT THIS CAN AND CANNOT DO — this bounds the whole feature:

  * Featherless serves TEXT and vision-language models only. It does
    NOT serve speech recognition, so nothing here can listen to a
    contribution. Any claim that AMAZWI "uses AI to check the audio"
    would be false while this is the only model integration present.
  * What it reads is TEXT that already exists: the card's target, the
    two typed peer answers, and the resolver's decision. That is a
    genuinely useful thing for a model to explain, and an honest one.

THE COUNCIL IS ADVISORY. It cannot overturn peer truth, cannot change a
contribution's state, and cannot move money. `app/council.py` writes its
output to `council_outputs` and nothing reads that back into the
resolver. This module must never gain a code path that does.

Three switches must ALL be on before a single byte leaves the machine:
`AI_COUNCIL_ENABLED=true`, a base URL, and an API key. A key sitting in
a `.env` is not consent to start spending someone's credit or sending
contribution text to a third party.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass

from app.config import AI_COUNCIL_ENABLED

REQUEST_TIMEOUT_SECONDS = 20


class LLMUnavailable(Exception):
    """No provider is configured, or the call failed.

    Callers must treat this as "fall back to the deterministic
    specialists", never as an error worth failing a resolution over --
    the Council is advisory and the golden path must not depend on it.
    """


@dataclass(frozen=True)
class ProviderConfig:
    name: str
    base_url: str
    api_key: str
    model: str
    task: str = "general"

    @property
    def is_configured(self) -> bool:
        return bool(self.base_url and self.api_key and self.model)


def _read(name: str) -> str:
    return (os.environ.get(name) or "").strip()


_PROVIDER_PREFIXES = {
    "groq": "AMAZWI_GROQ",
    "featherless": "AMAZWI_FEATHERLESS",
    "aiml": "AMAZWI_AIML",
}
_DEFAULT_PROVIDER_ORDER = {
    "fast": ("groq", "featherless", "aiml"),
    "reasoning": ("featherless", "aiml", "groq"),
    "general": ("groq", "featherless", "aiml"),
}


def resolve_provider(task: str = "general") -> ProviderConfig | None:
    """Pick a provider from the environment, or None.

    Task-aware routing is configurable. Fast tasks prefer Groq; reasoning
    tasks prefer Featherless; AIML remains an optional fallback. Returns None when the
    Council is disabled or nothing is fully configured -- never raises,
    because "not configured" is the normal state.
    """
    if not AI_COUNCIL_ENABLED:
        return None

    configured_order = tuple(
        name.strip().lower()
        for name in _read("AMAZWI_AI_PROVIDER_ORDER").split(",")
        if name.strip().lower() in _PROVIDER_PREFIXES
    )
    provider_order = configured_order or _DEFAULT_PROVIDER_ORDER.get(
        task, _DEFAULT_PROVIDER_ORDER["general"]
    )
    for name in provider_order:
        prefix = _PROVIDER_PREFIXES[name]
        config = ProviderConfig(
            name=name,
            base_url=_read(f"{prefix}_BASE_URL"),
            api_key=_read(f"{prefix}_API_KEY"),
            model=_read(f"{prefix}_MODEL"),
            task=task,
        )
        if config.is_configured:
            return config
    return None


def chat(
    messages: list[dict[str, str]],
    *,
    config: ProviderConfig | None = None,
    task: str = "general",
    max_tokens: int = 220,
    temperature: float = 0.2,
) -> str:
    """One OpenAI-compatible chat completion. Raises LLMUnavailable.

    Deliberately uses urllib rather than adding an SDK dependency: the
    request is one POST of one JSON body, and a new package in
    requirements.txt is a supply-chain decision this does not need.
    """
    config = config or resolve_provider(task)
    if config is None:
        raise LLMUnavailable("no LLM provider is configured")

    payload = json.dumps(
        {
            "model": config.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{config.base_url.rstrip('/')}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        # Never let the provider's key reach a log line or an exception
        # message that might be surfaced to a user.
        raise LLMUnavailable(f"{config.name} request failed: {type(exc).__name__}") from exc
    except json.JSONDecodeError as exc:
        raise LLMUnavailable(f"{config.name} returned a non-JSON body") from exc

    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise LLMUnavailable(f"{config.name} returned an unexpected shape") from exc

    if not isinstance(content, str) or not content.strip():
        raise LLMUnavailable(f"{config.name} returned empty content")
    return content.strip()


def explain_decision(
    *,
    language: str,
    target_word: str,
    peer_answers: list[str],
    understood: bool,
    config: ProviderConfig | None = None,
) -> str:
    """One plain sentence explaining a resolved contribution.

    The prompt states the decision as already made and asks only for an
    explanation, so the model has no room to appear to be deciding. It
    is given the peer answers because those ARE the evidence -- the
    model is describing peer truth, not replacing it.
    """
    verdict = "both listeners understood the speaker" if understood else "the two listeners did not agree"
    prompt = (
        f"Language: {language}. The speaker described the word '{target_word}' "
        f"without saying it. Two listeners independently typed: "
        f"{peer_answers[0]!r} and {peer_answers[1]!r}. "
        f"The decision has already been made by those two people: {verdict}. "
        "In one short sentence, explain that outcome to the speaker in plain "
        "English. Do not agree or disagree with the listeners, do not judge "
        "the pronunciation, and do not mention money."
    )
    return chat(
        [
            {
                "role": "system",
                "content": (
                    "You explain decisions that humans have already made. "
                    "You never make or reverse a decision."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        config=config,
        task="reasoning",
        max_tokens=120,
    )
