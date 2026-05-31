# Prompt Templates

These templates are designed for short Telegram messages that start one bounded
Codex task. They prefer reviewable output, explicit file-edit boundaries, and a
clear maintainer next step.

## How To Use These Templates

1. Pick the template that matches the maintainer job.
2. Replace placeholder URLs, logs, or repository names.
3. Keep secrets out of Telegram messages.
4. State whether file edits are allowed.
5. Keep one task per message.

## Templates

| Template | Use case |
|---|---|
| [Issue triage](../prompts/issue-triage.md) | Classify a GitHub issue and draft a first maintainer reply. |
| [Pull request review](../prompts/pr-review.md) | Get an actionable review pass before deeper local testing. |
| [Release checklist](../prompts/release-checklist.md) | Inspect a local checkout and prepare release readiness notes. |
| [CI failure triage](../prompts/ci-failure-triage.md) | Diagnose pasted logs or failing check links without editing files. |
| [Repository context review](../prompts/repo-context-review.md) | Evaluate whether an external repo matters to your roadmap. |

## Review Standard

Good Telegram Codex Bridge prompts usually include:

- the source of truth, such as an issue, PR, repo URL, pasted log, or local cwd
- the exact output shape you want
- the safety boundary: "Do not modify files" or "edits are allowed"
- verification commands when the answer may affect a release
- a request for findings before summary when reviewing code

## Follow-Up Pattern

For higher-risk workflows, use two messages instead of one:

1. Ask for diagnosis only, with no file edits.
2. After reviewing the answer, send a second prompt that allows a small scoped
   implementation.

This keeps mobile-triggered work bounded and easy to audit.
