# Live Workflow Runbook

This runbook prepares the maintainer dogfooding step that cannot be completed
by CI alone: sending real Telegram messages to the bridge and redacting the
results for public docs.

Use review-only mode unless you are intentionally testing local edits.

```env
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
```

Check `/status` in Telegram before each run. It should show the expected
version, working directory, model, search setting, and full-auto setting.

## Run 1: Issue Triage

Telegram message:

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

If there is no real issue yet, create or use a harmless test issue first, or
replace the URL with another public issue that is safe to discuss.

Evidence to capture:

- Telegram prompt
- bridge progress messages
- final Codex result
- whether files remained unchanged

## Run 2: Repository Context Review

Telegram message:

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

Evidence to capture:

- whether URL preprocessing found repository context
- final sourced-vs-inferred summary
- any limitations Codex reported

## Run 3: Release Checklist

Telegram message:

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
- release-note draft outline
- final go/no-go recommendation
```

Evidence to capture:

- final release-readiness summary
- commands suggested by Codex
- any mismatch between Codex's answer and actual repository state

## Redaction Checklist

Before copying a transcript into public docs, remove or replace:

- Telegram user IDs, chat IDs, bot names, and handles
- bot tokens, API keys, session identifiers, and local account names
- private absolute paths
- unrelated personal messages
- private repo URLs or issue links
- long logs that do not help readers understand the workflow

Use placeholders such as:

```text
[TELEGRAM_USER_ID]
[LOCAL_PATH]
[PRIVATE_TOKEN_REDACTED]
[PRIVATE_REPO]
```

## Public Transcript Shape

Keep public transcripts short and useful:

```text
Maintainer prompt:
...

Bridge progress:
- Codex started the task.
- Codex is planning the task.
- Codex completed the task.

Codex result:
...

Maintainer note:
No files were modified. The transcript was redacted before publication.
```

## Pass Criteria

A live workflow is useful enough to publish when:

- the bridge accepts the Telegram message from an allowed user
- Codex runs one bounded task
- the output matches the requested language and shape
- the task does not modify files when instructed not to
- the transcript can be redacted without losing the workflow story
