"""Environment-based configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    store_path: Path
    host: str
    port: int

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            store_path=Path(os.environ.get("TELEMETRY_STORE_PATH", "data/events.jsonl")),
            host=os.environ.get("TELEMETRY_HOST", "127.0.0.1"),
            port=int(os.environ.get("TELEMETRY_PORT", "8080")),
        )
