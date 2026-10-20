"""Append-only JSONL store with event_id deduplication."""
from __future__ import annotations

import json
import threading
from pathlib import Path

from .models import Event


class JsonlStore:
    def __init__(self, path: Path) -> None:
        self._path = Path(path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._seen: set[str] = set()
        self._load_existing()

    def _load_existing(self) -> None:
        if not self._path.exists():
            return
        with self._path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    self._seen.add(json.loads(line)["event_id"])

    def add(self, event: Event) -> bool:
        """Store the event. Returns False if event_id was already stored."""
        with self._lock:
            if event.event_id in self._seen:
                return False
            with self._path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
            self._seen.add(event.event_id)
            return True

    def __len__(self) -> int:
        return len(self._seen)
