# telemetry-ingest

A tiny Python 3.12 service that receives robot telemetry events over HTTP,
validates them, deduplicates by `event_id` (idempotency), and appends them to a
local JSONL store. ok

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export TELEMETRY_API_KEYS="dev-key-1,dev-key-2"   # comma-separated
python -m telemetry_ingest.service                 # listens on 127.0.0.1:8080
```

Send an event:

```bash
curl -X POST http://127.0.0.1:8080/events \
  -H "X-API-Key: dev-key-1" -H "Content-Type: application/json" \
  -d '{"event_id":"e-1","robot_id":"r-42","timestamp":"2025-01-01T12:00:00Z","kind":"battery","payload":{"level":0.87}}'
```

Responses: `201` stored, `200` duplicate (already stored), `400` invalid, `401` bad key.

## Configuration

| Variable | Default | Meaning |
|---|---|---|
| `TELEMETRY_API_KEYS` | (empty) | Comma-separated accepted API keys |
| `TELEMETRY_STORE_PATH` | `data/events.jsonl` | JSONL store location |
| `TELEMETRY_HOST` / `TELEMETRY_PORT` | `127.0.0.1` / `8080` | Bind address |

## Test

```bash
pip install pytest
python -m pytest
```

## Layout

```
src/telemetry_ingest/  models, store, service, config
auth/                  API key verification
infra/                 Dockerfile and illustrative deploy manifest
tests/                 pytest suite
.github/               CODEOWNERS and PR template
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) and [REVIEW_POLICY.md](REVIEW_POLICY.md).
