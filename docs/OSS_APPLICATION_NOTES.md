# Codex for Open Source Application Notes

These notes are draft material for the OpenAI Codex for Open Source
application form.

Official program page:

- https://openai.com/form/codex-for-oss/
- https://developers.openai.com/community/

## Repository

- Repository: https://github.com/Kyo14363/telegram-codex-bridge
- Role: primary maintainer
- Project stage: early public `v0.2.0` alpha release extracted from a working
  personal bridge

## Positioning

Telegram Codex Bridge is a self-hosted mobile control plane for Codex CLI.
It lets a maintainer send an authorized Telegram message, optionally fetch
URL/GitHub context, run one bounded local `codex exec --json` task, and receive
progress plus the result back in chat.

The project is aimed at small OSS maintainers who do not have a hosted
automation platform but still need a way to start review, triage, release, or
diagnostic workflows from mobile.

## Ecosystem Importance Argument

This repository is not applying on current stars or downloads. It is applying
as a reusable workflow pattern:

- Codex can already help with PR review, issue triage, release preparation, and
  local debugging.
- Many maintainers discover work from mobile notifications before they are at a
  development machine.
- A self-hosted Telegram bridge can turn those mobile interrupts into bounded,
  reviewable Codex tasks without requiring a new SaaS surface.
- The project favors conservative safety defaults: explicit user allowlist,
  repo-local runtime paths, and opt-in `--full-auto`.
- The public repository now includes a `v0.2.0` prerelease, prompt templates,
  workflow presets, a live workflow runbook, fresh-checkout verification notes,
  a redacted live Telegram dry-run transcript, CI sanity checks, and
  troubleshooting notes based on real dogfooding failures.

## Planned Use of API Credits

Credits would be used to harden and document real maintainer workflows:

- More real PR review examples and transcripts.
- Issue triage and reproduction-question drafting examples.
- Release checklist generation from a local checkout.
- GitHub/URL context fetching and source-aware summaries.
- Smoke/eval runs comparing safe mode against `--full-auto`.
- Security-oriented examples around allowlists, local command boundaries, and
  log redaction.

## Form Drafts

### Why does this repository qualify? (<=500 chars)

Telegram Codex Bridge is an early but focused maintainer tool: a self-hosted
Telegram control plane for Codex CLI. It helps maintainers triage issues, review
repo/URL context, run release checklists, and trigger bounded local Codex tasks
from mobile. Its ecosystem value is a reusable bridge pattern for mobile-first
OSS maintenance automation.

### How will you use API credits for your project? (<=500 chars)

API credits would fund dogfooding and examples for real maintainer workflows:
PR review prompts, issue triage, release-checklist automation, GitHub/URL
context fetching, and eval runs comparing safe vs full-auto Codex modes. The
goal is to turn the bridge from a personal tool into a documented, tested OSS
workflow kit for small maintainers.

### Anything else we should know? (<=500 chars)

This is a newly public repo extracted from a working personal bridge, so
stars/downloads are not the signal yet. I am applying early to accelerate
hardening: tests, docs, security defaults, GitHub Actions examples, and
maintainer workflows for mobile access to Codex without hosting a SaaS service.

## Suggested Repository Metadata

Description:

```text
Self-hosted Telegram bridge for running Codex CLI maintainer workflows from mobile.
```

Topics:

```text
codex, openai, telegram-bot, maintainer-tools, oss, developer-tools, automation, python
```

Website:

```text
https://openai.com/form/codex-for-oss/
```

## Near-Term Roadmap

- Add screenshots or transcripts showing each
  workflow end-to-end.
- Add more redacted live transcripts for issue triage, PR review, and release
  checklist workflows.
- Expand `docs/SECURITY.md` with platform-specific hardening notes for Windows,
  macOS, Linux, and containerized deployments.
- Add fresh virtual-environment verification on Windows and Linux.
- Add tests for more Codex event shapes and URL preprocessing edge cases.
- Add a sample `.env` walkthrough for Windows and Linux.
- Add screenshots showing a maintainer task from Telegram to Codex result.
