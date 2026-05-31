# Contributing

Thanks for helping improve Telegram Codex Bridge. This project is early, so the
most useful contributions are small, well-scoped, and tied to real maintainer
workflows.

## Good First Contributions

- Improve setup instructions from a fresh checkout.
- Add redacted workflow examples.
- Add smoke tests that do not require Telegram, network access, or live Codex
  calls.
- Improve safety docs around Telegram allowlists, `--full-auto`, and workspace
  boundaries.
- Add prompt templates for issue triage, PR review, release checklists, or CI
  failure diagnosis.

## Before Opening a PR

Run:

```powershell
python -m compileall .
python smoke_tests.py
```

If you change documentation only, still run the smoke tests once when possible
so the repo stays easy to verify.

## Safety Rules

- Do not commit `.env`, tokens, private logs, `runs/`, `fetch_outputs/`, or
  `stats.json`.
- Do not add defaults that broaden filesystem access.
- Keep `TCB_CODEX_FULL_AUTO=false` as the public default.
- Make risky behavior explicit and opt-in.
- Redact Telegram user IDs, private repository names, local paths, and secrets
  from examples.

## PR Shape

Keep PRs focused:

- one workflow improvement
- one bug fix
- one documentation pass
- one test expansion

Large refactors are easier to review after the relevant workflow or bug is
documented.

## Reporting Security Issues

Do not post active tokens, exploit details, or private logs in public issues.
See [SECURITY.md](SECURITY.md).
