"""API key verification using constant-time comparison."""
from __future__ import annotations

import hmac
import os

ENV_VAR = "TELEMETRY_API_KEYS"


class ApiKeyChecker:
    def __init__(self, keys: list[str]) -> None:
        self._keys = [k.encode() for k in keys if k]

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> "ApiKeyChecker":
        raw = (env if env is not None else os.environ).get(ENV_VAR, "")
        return cls([k.strip() for k in raw.split(",") if k.strip()])

    def is_valid(self, candidate: str | None) -> bool:
        if not candidate:
            return False
        cand = candidate.encode()
        # Check every key (no early exit) to keep timing independent of match position.
        result = False
        for key in self._keys:
            if hmac.compare_digest(cand, key):
                result = True
        return result
