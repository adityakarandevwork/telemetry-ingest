"""HTTP request handling (standard library only)."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Callable

from auth.api_keys import ApiKeyChecker

from .config import Config
from .models import Event, ValidationError
from .store import JsonlStore

MAX_BODY = 64 * 1024


def handle_event(
    body: bytes, api_key: str | None, checker: ApiKeyChecker, store: JsonlStore
) -> tuple[int, dict]:
    """Pure request logic: returns (status, json_body)."""
    if not checker.is_valid(api_key):
        return 401, {"error": "invalid api key"}
    try:
        event = Event.from_dict(json.loads(body))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 400, {"error": "body must be valid JSON"}
    except ValidationError as exc:
        return 400, {"error": str(exc)}
    if store.add(event):
        return 201, {"status": "stored", "event_id": event.event_id}
    return 200, {"status": "duplicate", "event_id": event.event_id}


def make_handler(checker: ApiKeyChecker, store: JsonlStore) -> Callable[..., BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self) -> None:
            if self.path == "/healthz":
                self._send(200, {"status": "ok"})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self) -> None:
            if self.path != "/events":
                self._send(404, {"error": "not found"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            if length > MAX_BODY:
                self._send(413, {"error": "body too large"})
                return
            body = self.rfile.read(length)
            status, resp = handle_event(body, self.headers.get("X-API-Key"), checker, store)
            self._send(status, resp)

    return Handler


def main() -> None:
    cfg = Config.from_env()
    server = ThreadingHTTPServer(
        (cfg.host, cfg.port), make_handler(ApiKeyChecker.from_env(), JsonlStore(cfg.store_path))
    )
    print(f"listening on {cfg.host}:{cfg.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
