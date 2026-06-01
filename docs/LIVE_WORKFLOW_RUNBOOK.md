# Live Workflow Evidence

This document summarizes the live Telegram dogfooding evidence behind Telegram
Codex Bridge. It is written for reviewers who want to understand why this
project is more than a thin bot wrapper.

Telegram Codex Bridge is not trying to replace first-party Codex mobile
experiences. Its value is as a small, auditable OSS reference implementation for
self-hosted, Telegram-native maintainer workflows.

## Reviewer Summary

The bridge turns a Telegram message from an allowed maintainer into one bounded
local `codex exec --json` task. The maintainer can start issue triage,
repository context review, or release readiness checks from mobile while the
actual Codex CLI process runs inside a local working directory.

The project has now been dogfooded through three public maintainer workflows:

| Workflow | What was tested | Evidence |
|---|---|---|
| Issue triage | Triage a public GitHub issue and draft a maintainer reply. | [Demo transcript](DEMO_TRANSCRIPT.md#live-issue-triage) |
| Repository context review | Review a public repository and separate sourced facts from inference. | [Demo transcript](DEMO_TRANSCRIPT.md#live-repository-context-review) |
| Release checklist | Inspect release readiness and identify stale docs/CI gaps. | [Demo transcript](DEMO_TRANSCRIPT.md#live-release-checklist) |

The release-checklist run produced a real no-go result: it found stale setup
verification docs, stale roadmap status, and missing package-build coverage in
CI. Those findings were fixed and released in `v0.2.1`.

## Why This Matters

Open-source maintenance often starts from mobile interruptions: an issue link,
CI failure, release blocker, or user report. First-party remote Codex
experiences are powerful, but this project explores a different OSS pattern:

- use a chat surface maintainers already have open
- keep the bridge self-hosted and inspectable
- keep workflows review-only by default
- preserve a clear local workspace boundary
- publish prompt templates, safety presets, redaction rules, and dogfooding
  transcripts that other maintainers can fork

The project is applying on ecosystem usefulness rather than current stars or
downloads. Its value is a reusable pattern that other maintainers can adapt to
Telegram, Discord, Slack, LINE, Claude Code, Codex CLI, local agents, CI triage,
release management, or narrow project-specific workflows.

## What Was Proved

### 1. Telegram Can Start A Bounded Codex Maintainer Task

The live issue-triage run used this prompt shape:

```text
Triage this issue for maintainer action:
https://github.com/Kyo14363/telegram-codex-bridge/issues/1

Do not modify files.

Return:
- likely category
- severity and user impact
- missing reproduction details
- likely owner area
- suggested labels
- draft maintainer reply
```

The bridge returned a structured triage result and draft maintainer reply. The
public transcript was redacted and added to [DEMO_TRANSCRIPT.md](DEMO_TRANSCRIPT.md).

### 2. URL/Repository Context Can Feed A Source-Aware Review

The repository-context run asked the bridge to inspect a public repository and
separate sourced facts from inference. The result explicitly distinguished what
came from repository context from what was inferred as maintainer-roadmap
analysis.

This matters because maintainer workflows often need lightweight external
context before deciding whether a deeper desktop review is worth the time.

### 3. Release Checklist Dogfooding Found Real Repository Drift

The release-checklist run asked Codex to inspect the local checkout without
editing files. It correctly returned a no-go recommendation because the repo had
stale verification docs and missing package-build coverage.

Follow-up fixes:

- `docs/SETUP_VERIFICATION.md` was updated from 7 to 10 smoke tests.
- `docs/ROADMAP.md` was updated to reflect completed dogfooding evidence.
- `docs/TROUBLESHOOTING.md` was updated to match the current test count.
- `python -m build` was added to CI.
- `v0.2.1` was released as a dogfooding evidence refresh.

This is the strongest evidence so far: the tool did not only produce a polished
demo answer; it identified maintainership work that needed to be done.

## Safety Posture

All public dogfooding runs used review-only settings:

```env
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
```

The public repository also includes:

- [Deployment security checklist](DEPLOYMENT_SECURITY_CHECKLIST.md)
- [Workflow presets](WORKFLOW_PRESETS.md)
- [Security guide](SECURITY.md)
- [Prompt templates](PROMPT_TEMPLATES.md)
- [Adoption guide](ADOPTION_GUIDE.md)
- [Platform setup notes](PLATFORM_SETUP.md)

The intended adoption path is conservative:

1. Start with review-only mode.
2. Use a dedicated working directory.
3. Keep `TCB_ALLOWED_USER_IDS` explicit.
4. Review runtime files before sharing transcripts.
5. Treat `TCB_CODEX_FULL_AUTO=true` as an advanced, scoped mode.

## Redaction Rules Used

Before copying Telegram output into public docs, remove or replace:

- Telegram user IDs, chat IDs, bot names, and handles
- bot tokens, API keys, session identifiers, and local account names
- private absolute paths
- unrelated personal messages
- private repo URLs or issue links
- fast-moving snapshot numbers that do not help readers understand the workflow

Use placeholders such as:

```text
[TELEGRAM_USER_ID]
[LOCAL_PATH]
[PRIVATE_TOKEN_REDACTED]
[PRIVATE_REPO]
<local model override>
```

## Reproduction Path

To reproduce the dogfooding workflow:

1. Install the bridge from a fresh clone.
2. Configure a Telegram bot token and `TCB_ALLOWED_USER_IDS`.
3. Keep review-only mode enabled.
4. Send one prompt from [Prompt templates](PROMPT_TEMPLATES.md).
5. Confirm `/status` shows the expected working directory and full-auto setting.
6. Capture the Telegram result.
7. Redact the transcript.
8. Verify `git status -sb` before publishing the transcript.

For local verification commands, see
[Fresh-checkout setup verification](SETUP_VERIFICATION.md).

## Application Framing

The honest application claim is:

> Telegram Codex Bridge is an early OSS reference implementation for
> self-hosted, Telegram-native maintainer workflows. It helps maintainers turn
> mobile interruptions into bounded Codex CLI tasks for issue triage, repository
> context review, and release readiness. Its value is not current adoption
> scale; it is a forkable, auditable bridge pattern with safety defaults,
> prompt templates, dogfooding transcripts, and cross-platform CI.

This framing does not claim to outperform first-party Codex mobile. It claims a
different niche: a simple, inspectable OSS pattern that other maintainers can
copy, modify, and specialize.
