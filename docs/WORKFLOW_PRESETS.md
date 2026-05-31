# Workflow Presets

Use these presets as starting points for common deployment modes. They are not
security guarantees; they are intended to make the bridge's operating mode
obvious before you start a task from Telegram.

## Review-Only Preset

Use this for first runs, demos, and read-only maintainer tasks.

```env
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
```

Recommended prompt boundary:

```text
Do not modify files. Inspect only and return findings first.
```

## URL Context Preset

Use this when the task starts from a GitHub, article, YouTube, X/Twitter, or
general web URL.

```env
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
TCB_GITHUB_README_MAX_LEN=8000
TCB_THIN_CONTENT_THRESHOLD=200
```

Recommended prompt boundary:

```text
Use the fetched context when it is useful. If the page is thin or dynamic, say
what evidence is missing instead of guessing.
```

## Local Maintainer Preset

Use this in a local repository checkout when Codex may inspect files and run
safe read-only commands.

```env
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=C:\path\to\repo
TCB_CODEX_EXTRA_DIRS=
```

Recommended prompt boundary:

```text
Inspect the current repo. Do not edit files. Return exact paths and verification
commands.
```

## Scoped Full-Auto Preset

Use this only when you intentionally want Codex to run commands and edit files
inside a trusted checkout.

```env
TCB_CODEX_FULL_AUTO=true
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=C:\path\to\repo
TCB_CODEX_EXTRA_DIRS=
```

Recommended prompt boundary:

```text
Make the smallest scoped change needed. Run focused verification. Do not touch
unrelated files.
```

## Choosing A Preset

| Task | Suggested preset |
|---|---|
| Issue or PR first pass | Review-only |
| External repo relevance check | URL context |
| Release readiness in a local checkout | Local maintainer |
| Small bug fix in a trusted checkout | Scoped full-auto |

Keep `TCB_ALLOWED_USER_IDS` set in every preset.
