import pytest

from app import llm


def enable_council(monkeypatch):
    monkeypatch.setattr(llm, "AI_COUNCIL_ENABLED", True)


def test_fast_task_prefers_groq_when_configured(monkeypatch):
    enable_council(monkeypatch)
    monkeypatch.setenv("AMAZWI_GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    monkeypatch.setenv("AMAZWI_GROQ_API_KEY", "groq-secret")
    monkeypatch.setenv("AMAZWI_GROQ_MODEL", "fast-model")
    monkeypatch.setenv("AMAZWI_FEATHERLESS_BASE_URL", "https://api.featherless.ai/v1")
    monkeypatch.setenv("AMAZWI_FEATHERLESS_API_KEY", "featherless-secret")
    monkeypatch.setenv("AMAZWI_FEATHERLESS_MODEL", "reasoning-model")

    config = llm.resolve_provider("fast")

    assert config is not None
    assert config.name == "groq"
    assert config.model == "fast-model"


def test_reasoning_task_prefers_featherless(monkeypatch):
    enable_council(monkeypatch)
    monkeypatch.setenv("AMAZWI_FEATHERLESS_BASE_URL", "https://api.featherless.ai/v1")
    monkeypatch.setenv("AMAZWI_FEATHERLESS_API_KEY", "featherless-secret")
    monkeypatch.setenv("AMAZWI_FEATHERLESS_MODEL", "reasoning-model")
    monkeypatch.setenv("AMAZWI_GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    monkeypatch.setenv("AMAZWI_GROQ_API_KEY", "groq-secret")
    monkeypatch.setenv("AMAZWI_GROQ_MODEL", "fast-model")

    config = llm.resolve_provider("reasoning")

    assert config is not None
    assert config.name == "featherless"


def test_general_task_uses_explicit_provider_order(monkeypatch):
    enable_council(monkeypatch)
    monkeypatch.setenv("AMAZWI_AI_PROVIDER_ORDER", "aiml, groq, unknown")
    monkeypatch.setenv("AMAZWI_GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    monkeypatch.setenv("AMAZWI_GROQ_API_KEY", "groq-secret")
    monkeypatch.setenv("AMAZWI_GROQ_MODEL", "fast-model")
    monkeypatch.setenv("AMAZWI_AIML_BASE_URL", "https://api.aimlapi.com/v1")
    monkeypatch.setenv("AMAZWI_AIML_API_KEY", "aiml-secret")
    monkeypatch.setenv("AMAZWI_AIML_MODEL", "fallback-model")

    config = llm.resolve_provider()

    assert config is not None
    assert config.name == "aiml"


def test_unconfigured_or_disabled_council_returns_none(monkeypatch):
    monkeypatch.setattr(llm, "AI_COUNCIL_ENABLED", False)
    monkeypatch.setenv("AMAZWI_GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    monkeypatch.setenv("AMAZWI_GROQ_API_KEY", "groq-secret")
    monkeypatch.setenv("AMAZWI_GROQ_MODEL", "fast-model")

    assert llm.resolve_provider("fast") is None


def test_provider_failure_never_leaks_api_key(monkeypatch):
    enable_council(monkeypatch)
    config = llm.ProviderConfig("groq", "https://127.0.0.1:1/v1", "secret-value", "model")

    with pytest.raises(llm.LLMUnavailable) as error:
        llm.chat([{"role": "user", "content": "hello"}], config=config)

    assert "secret-value" not in str(error.value)
