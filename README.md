# Telegram Codex Bridge

A self-hosted Telegram bridge for running Codex CLI maintainer workflows from
your phone.

The bridge receives an authorized Telegram message, optionally fetches context
from URLs or GitHub repository links, runs one bounded `codex exec --json` task
locally, and sends progress plus the final result back to Telegram.

## Why This Exists

Open-source maintenance often happens away from a desk: a maintainer sees an
issue, PR, release blocker, crash log, or user report on mobile and wants to
kick off a bounded engineering task immediately. Telegram Codex Bridge turns a
private Telegram bot into a small mobile control plane for Codex CLI.

Example maintainer workflows:

- Triage an issue link and draft a response.
- Review a GitHub repository or pull-request context from a URL.
- Ask Codex to inspect a local checkout and produce a release checklist.
- Fetch article, X/Twitter, YouTube, or GitHub context before a Codex task.
- Run a local diagnostic command through Codex and receive the summary in chat.

## Status

This is an early `v0.1.0` prerelease extracted from a personal bridge. It is
useful for maintainers who are comfortable self-hosting a Telegram bot and
running Codex CLI on their own machine. It is not a hosted service.

## Features

- Authorized Telegram text commands via `python-telegram-bot`
- One-shot Codex CLI tasks through `codex exec --json`
- Progress summaries from Codex JSON events
- Optional URL preprocessing for X/Twitter, YouTube, GitHub, and general pages
- File-backed metrics via `/stats`
- Process cancellation via `/cancel`
- Public-safe defaults: repo-local runtime folders and opt-in `--full-auto`

## Layout

| File | Role |
|---|---|
| `telegram_bridge_codex.py` | Entry point and Telegram application wiring |
| `config.py` | `.env` loading, runtime paths, safety switches, logging |
| `bridge_core.py` | Codex subprocess lifecycle, prompt building, event parsing |
| `handlers.py` | Telegram commands and message handling |
| `metrics.py` | Lightweight file-backed usage stats |
| `url_fetchers.py` | URL detection and content extraction helpers |
| `vision.py` | Optional Gemini Vision helper module |
| `smoke_tests.py` | Import and command-builder smoke tests |

## Setup

1. Install Python 3.11+.
2. Install the Codex CLI and make sure `codex` is available in `PATH`.
3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and fill in:

   ```env
   TELEGRAM_CODEX_BOT_TOKEN=123456:your_bot_token_here
   TCB_ALLOWED_USER_IDS=123456789
   ```

5. Start the bridge:

   ```powershell
   python telegram_bridge_codex.py
   ```

   On Windows, you can also run:

   ```powershell
   .\start_bridge.bat
   ```

## Core Settings

| Variable | Default | Meaning |
|---|---|---|
| `TELEGRAM_CODEX_BOT_TOKEN` | required | Telegram bot token from BotFather |
| `TCB_ALLOWED_USER_IDS` | empty | Comma/space-separated Telegram user IDs allowed to use the bot |
| `TCB_WORKING_DIR` | `.\workspace` | Directory passed to `codex exec -C` |
| `TCB_CODEX_EXTRA_DIRS` | empty | Semicolon-separated directories passed as `--add-dir` |
| `TCB_CODEX_MODEL` | empty | Optional Codex model override |
| `TCB_CODEX_SEARCH` | `false` | Whether to pass `--search` to Codex CLI |
| `TCB_CODEX_FULL_AUTO` | `false` | Whether to pass `--full-auto` to Codex CLI |
| `TCB_CODEX_TIMEOUT` | `1800` | Per-task timeout in seconds |

Relative path settings are resolved from the repository root, so
`TCB_WORKING_DIR=.\workspace` becomes a stable absolute path inside this
checkout.

## Commands

See [COMMANDS.md](COMMANDS.md).

## Documentation

- [Maintainer workflows](docs/WORKFLOWS.md)
- [Illustrative demo transcript](docs/DEMO_TRANSCRIPT.md)
- [Roadmap](docs/ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Security guide](docs/SECURITY.md)
- [Security policy](SECURITY.md)
- [Codex for Open Source notes](docs/OSS_APPLICATION_NOTES.md)

## Codex for Open Source

This project is being prepared for the Codex for Open Source program as an
early maintainer-workflow tool. Draft application notes live in
[docs/OSS_APPLICATION_NOTES.md](docs/OSS_APPLICATION_NOTES.md).

## Security Model

This project intentionally runs Codex CLI on your machine. Treat the Telegram
bot as a remote control for local engineering work.

- Always set `TCB_ALLOWED_USER_IDS`.
- Keep `.env` private.
- Use a dedicated working directory when trying the bridge for the first time.
- Leave `TCB_CODEX_FULL_AUTO=false` until you explicitly want unattended Codex
  shell commands and file edits.
- Review runtime files before sharing logs or `fetch_outputs/`.

## Development

Run smoke checks:

```powershell
python -m compileall .
python smoke_tests.py
```

The GitHub Actions workflow runs the same compile and smoke checks.
