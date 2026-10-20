from auth.api_keys import ApiKeyChecker


def test_valid_and_invalid():
    c = ApiKeyChecker.from_env({"TELEMETRY_API_KEYS": "k1, k2"})
    assert c.is_valid("k1") and c.is_valid("k2")
    assert not c.is_valid("k3")
    assert not c.is_valid("")
    assert not c.is_valid(None)


def test_no_keys_configured_rejects_all():
    assert not ApiKeyChecker.from_env({}).is_valid("anything")
