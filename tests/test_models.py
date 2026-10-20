import pytest

from telemetry_ingest.models import Event, ValidationError

GOOD = {"event_id": "e1", "robot_id": "r1", "timestamp": "2025-01-01T12:00:00Z", "kind": "battery", "payload": {"level": 0.5}}


def test_valid_event():
    assert Event.from_dict(GOOD).robot_id == "r1"


@pytest.mark.parametrize("field", ["event_id", "robot_id", "timestamp", "kind"])
def test_missing_field(field):
    data = {k: v for k, v in GOOD.items() if k != field}
    with pytest.raises(ValidationError):
        Event.from_dict(data)


def test_bad_kind_timestamp_payload():
    for patch in ({"kind": "nope"}, {"timestamp": "yesterday"}, {"payload": []}):
        with pytest.raises(ValidationError):
            Event.from_dict({**GOOD, **patch})


def test_not_an_object():
    with pytest.raises(ValidationError):
        Event.from_dict([1, 2])
