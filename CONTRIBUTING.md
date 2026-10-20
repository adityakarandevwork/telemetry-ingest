# Contributing

## Branch naming

Use `<type>/<short-description>`, where type is one of `feat`, `fix`, `docs`,
`chore`, `test`. Example: `fix/duplicate-event-status`.

## Pull requests

- Fill in the PR template (`.github/pull_request_template.md`).
- Keep PRs small and focused; include tests for behaviour changes.
- `python -m pytest` must pass.
- PRs touching protected paths (`auth/`, `infra/`, `.github/`) need a human
  maintainer approval. See [REVIEW_POLICY.md](REVIEW_POLICY.md).

## Style

Python 3.12, type hints, standard library first.
