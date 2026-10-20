"""Event model and validation."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

ALLOWED_KINDS = {"battery", "position", "error", "heartbeat"}
MAX_ID_LEN = 128


class ValidationError(ValueError):
    """Raised when an incoming event is malformed."""


@dataclass(frozen=True)
class Event:
    event_id: str
    robot_id: str
    timestamp: str
    kind: str
    payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Any) -> "Event":
        if not isinstance(data, dict):
            raise ValidationError("event must be a JSON object")
        for name in ("event_id", "robot_id", "timestamp", "kind"):
            value = data.get(name)
            if not isinstance(value, str) or not value:
                raise ValidationError(f"{name} is required and must be a non-empty string")
        for name in ("event_id", "robot_id"):
            if len(data[name]) > MAX_ID_LEN:
                raise ValidationError(f"{name} too long (max {MAX_ID_LEN})")
        if data["kind"] not in ALLOWED_KINDS:
            raise ValidationError(f"kind must be one of {sorted(ALLOWED_KINDS)}")
        try:
            datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValidationError("timestamp must be ISO 8601") from exc
        payload = data.get("payload", {})
        if not isinstance(payload, dict):
            raise ValidationError("payload must be an object")
        return cls(data["event_id"], data["robot_id"], data["timestamp"], data["kind"], payload)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
