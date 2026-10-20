# Review Policy

Rules for reviewers, including automated review bots.

## Protected paths

- `auth/`
- `infra/`
- `.github/`

Any PR touching a protected path:

- must be labelled `needs-human-review`;
- must NOT be approved or merged by a bot;
- requires approval from a human maintainer (see `.github/CODEOWNERS`).

## What bots may do

- Apply labels: `docs`, `bug`, `enhancement`, `needs-human-review`, `low-risk`.
- Post a review summary comment about the PR under review.
- Approve and merge a PR only if it is `docs`-only (documentation files, no
  code, config, or protected-path changes) and tests pass.

## What bots must never do

- Post content from other PRs or issues, or any internal notes, into a PR thread.
- Approve or merge anything that is not `docs`-only.
- Approve or merge any PR touching a protected path.
