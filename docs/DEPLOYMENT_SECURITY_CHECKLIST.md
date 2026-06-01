# Deployment Security Checklist

Use this checklist before pointing Telegram Codex Bridge at a real repository.

## Review-Only Demo

Recommended for first-time users and public demos.

- [ ] `TCB_ALLOWED_USER_IDS` is set to known Telegram user IDs.
- [ ] `TCB_CODEX_FULL_AUTO=false`.
- [ ] `TCB_CODEX_SEARCH=false` unless search is required for the demo.
- [ ] `TCB_WORKING_DIR` points to a dedicated workspace.
- [ ] `.env`, `logs/`, `runs/`, `fetch_outputs/`, and `stats.json` are ignored.
- [ ] Demo prompts say "Do not modify files."
- [ ] Screenshots and transcripts are redacted before publication.

## Local Maintainer Mode

Use this when the bridge may inspect a local checkout but should not edit files.

- [ ] The checkout is dedicated to this project or task.
- [ ] The working directory is not a home folder, desktop, cloud-drive root, or
      secrets directory.
- [ ] `TCB_CODEX_EXTRA_DIRS` is empty unless a task genuinely needs extra files.
- [ ] Prompts ask for findings, plans, or checklists before implementation.
- [ ] Important results are verified from the desktop before acting on them.
- [ ] Runtime files are reviewed before sharing with issue reporters.

## Scoped Full-Auto Mode

Use this only when you intentionally want Codex to run commands and edit files.

- [ ] The working tree is clean before starting.
- [ ] You are willing to review every diff before commit.
- [ ] The prompt names the exact scope and files or behavior to change.
- [ ] The prompt excludes unrelated refactors.
- [ ] You have a recovery path such as git history or a disposable checkout.
- [ ] Full-auto is turned off again after the task if it is not your default
      operating mode.

## Token And Secret Hygiene

- [ ] The Telegram bot token exists only in `.env` or a local secret manager.
- [ ] `.env` has never been committed.
- [ ] Logs and transcripts do not contain bot tokens, API keys, session IDs, or
      private repository links.
- [ ] Bot tokens are rotated after accidental exposure.
- [ ] Screenshots crop out chat IDs, user IDs, bot handles, and unrelated
      private messages.

## Incident Response

If something goes wrong:

1. Run `/cancel` in Telegram.
2. Stop the local bridge process.
3. Rotate the Telegram bot token if exposure is possible.
4. Review `logs/`, `runs/`, `fetch_outputs/`, and git diffs.
5. File a minimal public issue only after removing private details.

## Release Gate

Before a public release:

- [ ] `python -m ruff check .`
- [ ] `python -m compileall -q .`
- [ ] `python smoke_tests.py`
- [ ] `python scripts/sanity_check.py`
- [ ] `python -m build`
- [ ] Fresh-checkout verification has been updated if behavior changed.
- [ ] Demo transcripts have been reviewed for private data.
