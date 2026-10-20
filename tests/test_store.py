import json

from telemetry_ingest.models import Event
from telemetry_ingest.store import JsonlStore


def ev(i="e1"):
    return Event(i, "r1", "2025-01-01T12:00:00Z", "heartbeat")


def test_dedupe(tmp_path):
    store = JsonlStore(tmp_path / "events.jsonl")
    assert store.add(ev()) is True
    assert store.add(ev()) is False
    assert len(store) == 1
    assert len((tmp_path / "events.jsonl").read_text().splitlines()) == 1


def test_dedupe_survives_restart(tmp_path):
    path = tmp_path / "events.jsonl"
    JsonlStore(path).add(ev())
    again = JsonlStore(path)
    assert again.add(ev()) is False
    assert again.add(ev("e2")) is True
    assert json.loads(path.read_text().splitlines()[0])["event_id"] == "e1"
