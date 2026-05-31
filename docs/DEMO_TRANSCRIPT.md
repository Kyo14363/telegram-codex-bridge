# Demo Transcript

This is an illustrative transcript for the current public skeleton. It is not a
production log and does not contain private tokens, real issue data, or local
workspace paths.

The goal is to show the maintainer experience the project is designed around:
start from Telegram, let the bridge gather lightweight context, run one bounded
Codex task, and return a reviewable result.

## Setup Used

```env
TCB_ALLOWED_USER_IDS=123456789
TCB_CODEX_FULL_AUTO=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_SEARCH=false
```

## Scenario 1: Issue Triage

Maintainer sends:

```text
Triage this issue for maintainer action:
https://github.com/example/project/issues/123

Return:
- likely category
- missing reproduction details
- risk level
- draft maintainer reply
- suggested labels
Do not modify files.
```

Bridge replies:

```text
Fetching URL context, then starting Codex...
```

Progress update:

```text
Codex is working...
Codex started the task.
```

Progress update:

```text
Codex is working...
Codex is using a tool: local command
```

Final response:

```text
Codex result

Likely category: bug report / needs reproduction

Missing details:
- exact package version
- operating system and runtime version
- minimal reproduction repository or snippet
- expected behavior vs actual behavior
- full stack trace as text, not screenshot

Risk level: medium

Suggested labels:
- bug
- needs reproduction
- needs info

Draft maintainer reply:

Thanks for the report. Could you share the exact package version, runtime
version, operating system, and a minimal reproduction? The current description
points to a possible regression, but we need a reproducible case before we can
confirm the owner area.
```

Maintainer action:

- Paste the reply into GitHub.
- Add labels.
- Wait for reproduction details before asking Codex to inspect code.

## Scenario 2: Release Checklist

Maintainer sends:

```text
In the current working directory, prepare a release checklist.

Inspect the repo state, recent commits, test commands, docs, and packaging
files. Do not change files. Return:
- readiness summary
- blockers
- suggested verification commands
- changelog/release-note draft outline
```

Bridge progress:

```text
Codex is working...
Codex started the task.
```

Bridge progress:

```text
Codex is working...
Codex is running a local command: git status --short
```

Final response:

```text
Codex result

Readiness summary:
The repository appears close to a docs-only public skeleton release. The main
blocking items are validation of the install path, one real Telegram dry run,
and a tag/release note.

Blockers:
- no tagged release yet
- setup instructions have not been tested on a fresh checkout
- no real transcript from a live Telegram bot run

Suggested verification commands:
- python -m pip install -r requirements.txt
- python -m compileall .
- python smoke_tests.py
- python telegram_bridge_codex.py

Release-note outline:
- public-safe repo skeleton
- maintainer workflow docs
- safety defaults
- CI smoke checks
```

Maintainer action:

- Run the verification commands locally.
- Tag a release after a real dry run.
- Replace this illustrative transcript with a real redacted transcript.

## Scenario 3: PR Review Prompt

Maintainer sends:

```text
Review this pull request from a maintainer perspective:
https://github.com/example/project/pull/456

Focus on:
- behavioral regressions
- missing tests
- security or data-loss risks
- unclear migration or release notes

Return only actionable findings first, then a short summary.
```

Final response shape:

```text
Codex result

Findings:
- P1: The migration path does not cover existing config files...
- P2: The new parser path has no test for malformed input...

Open questions:
- Should this behavior remain backward-compatible for v1 users?

Summary:
The PR is directionally reasonable but needs one migration test and a clearer
release note before merge.
```

Maintainer action:

- Use the findings as a first-pass checklist.
- Re-run project tests before posting review comments.

## Notes for Future Real Demos

Replace this illustrative file with a redacted live transcript after:

- creating a dedicated demo Telegram bot
- using a disposable repository checkout
- setting `TCB_CODEX_FULL_AUTO=false`
- redacting user IDs, tokens, private paths, and repo secrets
