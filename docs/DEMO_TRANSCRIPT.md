# Demo Transcript

This file contains redacted live dogfooding runs plus short illustrative
workflow examples. It does not contain private tokens, Telegram user IDs,
private issue data, or private workspace paths.

The goal is to show the maintainer experience this project is designed around:
start from Telegram, let the bridge gather lightweight context, run one bounded
Codex task, and return a reviewable result.

## Safety Settings

The live runs below used review-only settings.

```env
TCB_ALLOWED_USER_IDS=<one allowed Telegram user>
TCB_CODEX_MODEL=gpt-5.4
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
```

## Live Dry Run

Date: 2026-05-31

Maintainer sends from Telegram:

```text
Ask for a short telegram-codex-bridge dry-run status summary. Do not modify
files.
```

Bridge command shape:

```text
codex exec --json --skip-git-repo-check -C <repo>\workspace -o <repo>\runs\codex-last-20260531-182934.txt -m gpt-5.4 -
```

Telegram receives, translated from the original Traditional Chinese result:

```text
Codex result

Status summary: this is a telegram-codex-bridge v0.1.0 dry run. The message was
handled successfully. This run only returns a status response and did not modify
files or perform write operations.
```

Observed outcome:

- Telegram polling worked.
- The allowlist accepted the maintainer's Telegram account.
- Codex CLI launched through the bridge.
- The bridge wrote the prompt and final output into `runs/`.
- `TCB_CODEX_FULL_AUTO=false` stayed in effect.
- No files were modified by the Codex task.

Two issues were found and fixed during the live dry run:

- Relative runtime paths must resolve from the repository root before passing
  them to Codex. This prevents `workspace\workspace` style failures.
- Some Codex CLI installs may reject their default model. The local dry run set
  `TCB_CODEX_MODEL=gpt-5.4`, and the public docs now explain this compatibility
  setting.

## Live Issue Triage

Date: 2026-05-31

Source issue:

```text
https://github.com/Kyo14363/telegram-codex-bridge/issues/1
```

Maintainer sends:

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

Keep the reply polite, specific, and easy to paste into GitHub.
```

Captured bridge progress:

```text
Only the final Telegram result was captured for this run.
```

Telegram receives:

```text
Codex result

Based on issue #1 and the repo README snapshot, this looks like a maintainer
workflow-validation issue rather than a product bug.

- Likely category: documentation / dogfooding / maintainer-workflow validation
- Severity and user impact: Low
  - No end-user-facing product regression is described.
  - Impact is mainly on maintainer confidence, runbook quality, and whether the
    Telegram-to-Codex triage flow works as documented.
- Missing reproduction details:
  - Exact bridge version or commit used for the dogfood run
  - Codex CLI version and model, if relevant
  - Exact Telegram prompt/message sent to the bot
  - Whether URL preprocessing was enabled and what context was injected
  - Runtime settings that may affect behavior, especially TCB_CODEX_SEARCH and
    TCB_CODEX_FULL_AUTO
  - Actual observed output vs expected output, if the workflow fails
  - Confirmation method for "no local files modified"
  - Link or location of the redacted transcript once captured
- Likely owner area:
  - Maintainer tooling / workflow docs
  - Likely code areas: Telegram message handling, Codex task execution, URL
    preprocessing, and runbook/docs
- Suggested labels:
  - documentation
  - workflow
  - dogfood
  - maintainer-tooling
  - low-risk

Draft maintainer reply:

Thanks for opening this. I am triaging it as a workflow-validation/documentation
issue rather than a product bug.

The goal here is clear: verify that the Telegram bridge can accept the issue
URL, run one bounded review-only Codex task, and return a structured triage
result without modifying local files.

Proposed maintainer action:
1. Label this as documentation/workflow dogfood.
2. Run the issue through the Telegram bridge in review-only mode.
3. Save a redacted transcript for the live workflow runbook.
4. Close once the documentation evidence is captured, or convert into a bug if
   the run exposes a real failure.
```

Observed outcome:

- The bridge returned a structured issue triage result.
- The response matched the requested issue-triage shape.
- The output did not include private tokens, Telegram IDs, or local account
  paths.
- `git status -sb` showed no tracked repository changes immediately before
  this transcript was added.

## Live Repository Context Review

Date: 2026-05-31

Source repository:

```text
https://github.com/openai/openai-python
```

Maintainer sends:

```text
Read this repository and tell me whether it is relevant to our maintainer
tooling roadmap:
https://github.com/openai/openai-python

Do not modify files.

Summarize:
- what the repository does
- maintenance activity signals
- integration ideas
- risks or incompatibilities
- whether it is worth a deeper desktop review

Separate sourced facts from inference.
```

Captured bridge progress:

```text
Only the final Telegram result was captured for this run.
```

Telegram receives, abridged from the original Traditional Chinese result:

```text
Codex result

No local workspace files were inspected or modified. The task only read remote
GitHub repository content and GitHub metadata.

Sourced facts:
- openai/openai-python is the official Python SDK for the OpenAI API.
- It supports sync and async clients, type definitions, streaming, Realtime,
  webhook verification, Azure OpenAI, and workload identity authentication.
- The README and source headers describe the SDK as generated from an OpenAPI
  spec by Stainless.
- Maintenance signals suggest an active generated-SDK workflow: recent release
  and documentation commits, CI split into lint/build/test/examples, contribution
  docs that call out generated code, and release/publish workflows.

Inference:
The repository is a strong reference sample for generated SDK maintenance, but
not a generic maintainer platform by itself.

Integration ideas:
- Use a generated/manual boundary model as inspiration for review routing and
  conflict checks.
- Study CI splitting for lint/build/test/examples and conditional codegen paths.
- Treat release PR and publish workflows as examples for release automation.
- Use issue/PR clusters as a possible regression-triage corpus.

Risks or incompatibilities:
- Many patterns are specific to OpenAPI and Stainless-generated SDKs.
- Some workflow pieces depend on project-specific infrastructure.
- The contribution model reflects a controlled generation pipeline more than a
  broad community-PR workflow.

Deeper review recommendation:
Worth it if the roadmap includes codegen repo maintenance, release automation,
generated/manual boundary enforcement, or SDK compatibility triage. Keep the
review scoped to .github/workflows, CONTRIBUTING.md, the PR template, and recent
issues/PRs before doing a full code read.
```

Observed outcome:

- The bridge produced a source-aware repository review.
- The answer separated sourced facts from inference.
- The output explicitly stated that local workspace files were not inspected or
  modified.
- Fast-moving snapshot details such as stars, forks, current version, and recent
  commit dates were omitted from this public transcript because they become stale
  quickly. The dated run still captures the workflow behavior.

## Live Release Checklist

Date: 2026-05-31

Maintainer sends:

```text
In the current working directory, prepare a release checklist.

Do not modify files.

Inspect:
- repo status and recent commits
- changelog and version markers
- packaging or install metadata
- test and lint commands
- docs that should be updated before release

Return:
- readiness summary
- blockers
- suggested verification commands
- changelog/release-note draft outline
- final go/no-go recommendation
```

Captured bridge progress:

```text
Only the final Telegram result was captured for this run.
```

Telegram receives, abridged:

```text
Codex result

Readiness summary:
The worktree is clean on main...origin/main. Recent commits are mostly
docs/dogfooding focused, while the last code-and-metadata-heavy release commit
is the v0.2 workflow kit. The release surface is in decent shape:
pyproject.toml defines package metadata, config.py and README identify the
project version, CHANGELOG.md has unreleased entries, and CI covers install,
lint, compile, smoke, and sanity checks.

Blockers:
- CHANGELOG.md still has unreleased items while config.py and pyproject.toml
  remain at v0.2.0.
- docs/SETUP_VERIFICATION.md is stale: it still reports 7 smoke tests, while
  the current suite has 10.
- docs/ROADMAP.md is stale: it leaves contributor guide and real-world
  dogfooding examples unchecked even though they now exist.
- Package build verification is not part of CI. This is not a blocker for a
  source-only GitHub release, but it matters if built artifacts are intended.

Suggested verification commands:
- python -m pip install -r requirements.txt
- python -m pip install -e ".[dev]"
- python -m ruff check .
- python -m compileall -q .
- python smoke_tests.py
- python scripts/sanity_check.py
- python -m pip install build
- python -m build

Release-note draft:
If releasing current HEAD, v0.2.1 is more defensible than v0.3.0 based on
visible scope. It looks like a documentation and dogfooding evidence refresh for
the maintainer workflow kit.

Go/no-go recommendation:
No-go yet. Decide and stamp the next version, move changelog entries out of
Unreleased, refresh stale verification/docs entries, rerun checks, and then cut
a small v0.2.1 alpha-style release.
```

Observed outcome:

- The bridge produced a release checklist with concrete blockers.
- The checklist found real stale documentation in the repository.
- The response recommended a conservative `v0.2.1` follow-up rather than
  overclaiming `v0.3.0`.
- The blockers were addressed after this run by refreshing setup verification,
  roadmap status, changelog/version markers, and CI package-build coverage.

## Illustrative Release Checklist

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

Expected response shape:

```text
Codex result

Readiness summary:
The repository appears close to a public prerelease. The main checks are install
verification, a real Telegram dry run, and release notes.

Blockers:
- setup instructions need fresh-checkout verification
- demo transcript needs redaction review

Suggested verification commands:
- python -m pip install -e ".[dev]"
- python -m ruff check .
- python -m compileall -q .
- python smoke_tests.py
- python scripts/sanity_check.py
```

Maintainer action:

- Run the verification commands locally.
- Tag a release after live dogfooding evidence is captured.

## Illustrative PR Review Prompt

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

Expected response shape:

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
