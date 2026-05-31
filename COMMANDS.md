# Commands

Telegram Codex Bridge is intentionally small. Text messages become one
non-interactive `codex exec --json` task, and the bridge reports lightweight
progress back to Telegram.

| Command | Purpose |
|---|---|
| `/start` | Show startup status. |
| `/help` | Show command help. |
| `/status` | Show bridge state, cwd, model, search, and full-auto setting. |
| `/stats` | Show lightweight usage metrics. |
| `/cwd` | Show the Codex working directory and extra directories. |
| `/cancel` | Stop the active Codex process tree. |
| `/clear` | Alias for `/cancel`. |
| `/bridge [n]` | Show the last `n` bridge log lines, capped at 120. |
| `/ps` | Show local `python`, `node`, and `codex` process summaries. |

## Example Prompts

```text
Review this GitHub repository and summarize whether it looks maintained:
https://github.com/example/project
```

```text
Read this issue link and draft a triage response with reproduction questions.
https://github.com/example/project/issues/123
```

```text
Create a release checklist for the current repo in the working directory.
```

```text
Inspect the latest failing test log in the workspace and suggest the smallest fix.
```

## Safety Notes

- Set `TCB_ALLOWED_USER_IDS`; otherwise anyone who can message the bot can run
  tasks through your bridge.
- `TCB_CODEX_FULL_AUTO=false` is the public default. Enable it only for local
  workspaces where unattended Codex file edits and shell commands are acceptable.
- Do not commit `.env`, `logs/`, `runs/`, `fetch_outputs/`, `stats.json`, or
  private workspace files.
