# Maintainer Workflows

Telegram Codex Bridge is designed for bounded maintainer tasks that can start
from a mobile message and finish as a reviewable Codex CLI result.

Each workflow below follows the same pattern:

1. Send a Telegram message to the bot.
2. The bridge optionally fetches URL or GitHub context.
3. The bridge runs one `codex exec --json` task in `TCB_WORKING_DIR`.
4. Telegram receives progress summaries and the final Codex answer.

## Safety Presets

Use these presets before trying the workflows.

See [Workflow presets](WORKFLOW_PRESETS.md) for copyable environment examples,
and [Prompt templates](PROMPT_TEMPLATES.md) for standalone maintainer prompts.
When you are ready to capture public dogfooding evidence, use the
[Live workflow runbook](LIVE_WORKFLOW_RUNBOOK.md).

### Review-only mode

Recommended for first runs and public demos.

```env
TCB_CODEX_FULL_AUTO=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
```

Ask Codex to inspect, summarize, draft, or plan. Avoid prompts that request file
edits until you are comfortable with the workspace boundary.

### Maintainer mode

Use this only in a checkout where Codex may run local commands and edit files.

```env
TCB_CODEX_FULL_AUTO=true
TCB_WORKING_DIR=C:\path\to\your\repo
TCB_CODEX_EXTRA_DIRS=
```

Keep the Telegram allowlist strict and review every resulting diff before
committing.

## Workflow 1: Issue Triage

Use when a maintainer receives an issue link on mobile and wants a fast,
structured first pass.

Telegram prompt:

```text
Triage this issue for maintainer action:
https://github.com/OWNER/REPO/issues/123

Return:
- likely category
- missing reproduction details
- risk level
- draft maintainer reply
- suggested labels
Do not modify files.
```

Expected result:

- A concise issue category such as bug, feature request, docs, support, or
  needs reproduction.
- Specific reproduction questions.
- A reply draft that can be pasted into GitHub.
- No local file changes.

## Workflow 2: Pull Request Review

Use when a PR needs a lightweight review pass before deeper local testing.

Telegram prompt:

```text
Review this pull request from a maintainer perspective:
https://github.com/OWNER/REPO/pull/456

Focus on:
- behavioral regressions
- missing tests
- security or data-loss risks
- unclear migration or release notes

Return only actionable findings first, then a short summary.
```

Expected result:

- Findings ordered by severity.
- Concrete file or behavior references when available.
- Suggested follow-up tests.
- A summary that can guide the maintainer's next review pass.

## Workflow 3: Release Checklist

Use in a local checkout when preparing a release.

Telegram prompt:

```text
In the current working directory, prepare a release checklist.

Inspect the repo state, recent commits, test commands, docs, and packaging
files. Do not change files. Return:
- readiness summary
- blockers
- suggested verification commands
- changelog/release-note draft outline
```

Expected result:

- A release readiness summary.
- A checklist of tests and packaging checks.
- A list of missing documentation or changelog items.
- No local file changes unless explicitly requested.

## Workflow 4: CI Failure Triage

Use when a failing check, pasted log, or log URL needs a first-pass diagnosis.

Telegram prompt:

```text
Investigate this failing CI log and propose the smallest likely fix:
PASTE_LOG_OR_URL_HERE

Return:
- suspected root cause
- evidence from the log
- minimal fix plan
- commands to verify locally
Do not edit files yet.
```

Expected result:

- A root-cause hypothesis tied to log evidence.
- A minimal verification path.
- A clear boundary between diagnosis and file edits.

## Workflow 5: URL or Repository Context Review

Use when you need Codex to inspect an external URL before deciding whether it
matters to your project.

Telegram prompt:

```text
Read this repository and tell me whether it is relevant to our maintainer
tooling roadmap:
https://github.com/OWNER/REPO

Summarize:
- what it does
- maintenance activity signals
- integration ideas
- risks or incompatibilities
```

Expected result:

- Bridge-fetched README or metadata context when available.
- A source-aware summary.
- Practical integration and risk notes.

## Workflow 6: Mobile Incident Follow-Up

Use when a user report arrives while the maintainer is away from the desktop.

Telegram prompt:

```text
Prepare a first-response plan for this user report:
PASTE_REPORT_HERE

Assume I am on mobile. Return:
- immediate clarifying questions
- logs or environment details to request
- likely owner area
- a polite reply draft
```

Expected result:

- A reply that buys time without overpromising.
- Specific evidence requests.
- A later desktop investigation checklist.

## Prompt Design Rules

- State whether file edits are allowed.
- State whether Codex should run commands or only inspect.
- Ask for findings before summary when reviewing code.
- Ask for exact verification commands when diagnosing failures.
- Keep secrets out of Telegram messages.
- Prefer one bounded task per message.

## Output Review

Before acting on a Codex result:

- Check whether the answer relied on fetched context, local files, or inference.
- Re-run important commands locally when the task affects releases, security,
  or data.
- Review generated diffs before committing.
- Keep runtime files such as `runs/`, `logs/`, and `fetch_outputs/` private.
