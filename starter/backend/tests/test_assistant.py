from app.assistant import handle_assistant_message


def test_navigates_to_rewards_from_natural_language():
    result = handle_assistant_message("Please take me to my rewards", "en")

    assert result.intent == "NAVIGATE"
    assert result.route == "/rewards"
    assert result.advisory is True
    assert result.provider == "deterministic"


def test_explains_receipt_without_claiming_provider_settlement():
    result = handle_assistant_message("Why did I earn this?", "en")

    assert result.intent == "EXPLAIN_RECEIPT"
    assert result.route == "/rewards"
    assert "human" in result.reply.lower()
    assert "settlement" in result.reply.lower()


def test_sensitive_payment_request_is_refused_without_route():
    result = handle_assistant_message("Cash me out and send the money now", "en")

    assert result.intent == "PAYMENT_CONFIRMATION_REQUIRED"
    assert result.route is None
    assert "cannot" in result.reply.lower()
    assert result.advisory is True


def test_unknown_request_has_safe_help_without_model_call():
    result = handle_assistant_message("Tell me something unrelated", "en")

    assert result.intent == "HELP"
    assert result.route is None
    assert result.provider == "deterministic"
    assert "play" in result.reply.lower()
