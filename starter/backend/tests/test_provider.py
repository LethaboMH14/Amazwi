from app.provider import DemoProvider, PaymentState


def test_submit_is_idempotent():
    provider = DemoProvider()
    a = provider.submit("user-1", 200, "key-1")
    b = provider.submit("user-1", 200, "key-1")
    assert a.id == b.id


def test_status_resolves_to_paid():
    provider = DemoProvider()
    attempt = provider.submit("user-1", 200, "key-2")
    resolved = provider.get_status(attempt.id)
    assert resolved.state == PaymentState.PAID
