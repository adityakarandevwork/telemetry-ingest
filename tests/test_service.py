import json

from auth.api_keys import ApiKeyChecker
from telemetry_ingest.service import handle_event
from telemetry_ingest.store import JsonlStore

BODY = json.dumps({"event_id": "e1", "robot_id": "r1", "timestamp": "2025-01-01T12:00:00Z", "kind": "error"}).encode()


def test_flow(tmp_path):
    checker = ApiKeyChecker(["k"])
    store = JsonlStore(tmp_path / "e.jsonl")
    assert handle_event(BODY, "bad", checker, store)[0] == 401
    assert handle_event(b"{", "k", checker, store)[0] == 400
    assert handle_event(BODY, "k", checker, store)[0] == 201
    assert handle_event(BODY, "k", checker, store)[0] == 200
