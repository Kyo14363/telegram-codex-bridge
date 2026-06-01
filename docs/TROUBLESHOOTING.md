# Troubleshooting

This guide collects issues seen during local dogfooding and likely setup
mistakes for new users.

## Missing Telegram Bot Token

Symptom:

```text
Missing TELEGRAM_CODEX_BOT_TOKEN
```

Fix:

```env
TELEGRAM_CODEX_BOT_TOKEN=123456:your_bot_token_here
```

You can put this in `.env` or in your local environment. Never commit a real
bot token.

## Unauthorized Telegram User

Symptom:

```text
Unauthorized. Your Telegram user id is: ...
```

Fix:

Add your Telegram user ID to the allowlist:

```env
TCB_ALLOWED_USER_IDS=123456789
```

Leaving the allowlist empty is convenient for experiments but unsafe for real
use.

## Telegram 409 Conflict

Symptom:

```text
Conflict: terminated by other getUpdates request
```

Cause:

Two processes are polling the same Telegram bot token.

Fix:

- Stop duplicate bridge processes.
- Use a separate bot token for each bridge instance.
- Avoid double-clicking `start_bridge.bat` while another copy is already
  running.

Useful Windows check:

```powershell
Get-CimInstance Win32_Process |
  Where-Object { $_.CommandLine -match 'telegram_bridge_codex.py' } |
  Select-Object ProcessId,Name,CommandLine
```

## `os error 2` When Starting Codex

Symptom:

```text
Codex process returned a non-zero exit code.
stderr tail:
Error: The system cannot find the file specified. (os error 2)
```

Cause observed during dogfooding:

The bridge was using a relative `TCB_WORKING_DIR` as both the subprocess working
directory and the `codex exec -C` argument. That made Codex look for a nested
path such as `workspace\workspace`.

Fix:

Use v0.1.1 or later. Relative runtime paths are now resolved from the repository
root before they are passed to Codex.

Recommended setting:

```env
TCB_WORKING_DIR=.\workspace
```

Expected resolved path:

```text
<repo>\workspace
```

## Codex Default Model Is Unsupported

Symptom:

```text
The 'gpt-5.5' model requires a newer version of Codex.
Please upgrade to the latest app or CLI and try again.
```

Cause:

Your installed Codex CLI may have a default model that the local CLI version
cannot run.

Fix options:

1. Upgrade Codex CLI.
2. Set an explicit model supported by your installed CLI:

```env
TCB_CODEX_MODEL=<known-supported-model>
```

The live dry run used this compatibility setting with a locally supported model.

## Codex Produces No Final Output

Symptom:

```text
(Codex produced no final output.)
```

Likely causes:

- Codex failed before writing the output file.
- The model was unsupported.
- The working directory was invalid.
- Codex timed out before producing a final answer.

Check:

- `logs/bridge.log`
- `runs/codex-prompt-*.txt`
- `runs/codex-last-*.txt`
- `/stats` in Telegram

## PowerShell Shows `NativeCommandError` Even Though Tests Passed

Symptom:

PowerShell wraps unittest output like this:

```text
NativeCommandError
Ran 10 tests
OK
```

Cause:

Some tools write progress or test dots to stderr. PowerShell can display that as
a native command error even when the process exit code is zero.

Fix:

Check the final test result and exit code. In this repository, successful smoke
tests end with:

```text
Ran 10 tests
OK
```

## Chinese Text Looks Garbled in PowerShell Logs

Symptom:

Chinese output appears as mojibake in PowerShell but looks correct in Telegram.

Cause:

Console encoding/display mismatch. The prompt and output files are UTF-8.

Check with Python:

```powershell
python -c "from pathlib import Path; print(Path('runs/YOUR_FILE.txt').read_text(encoding='utf-8'))"
```

## Runtime Files Contain Private Data

The bridge can write prompts, URLs, source snippets, and AI outputs into:

- `logs/`
- `runs/`
- `fetch_outputs/`
- `stats.json`

These paths are ignored by git. Redact them before sharing.

## Resetting a Local Dry Run

For a clean local retry:

1. Stop any running `telegram_bridge_codex.py` process.
2. Keep `.env` but review `TCB_CODEX_MODEL`, `TCB_WORKING_DIR`, and
   `TCB_ALLOWED_USER_IDS`.
3. Delete local-only runtime folders if needed:

```powershell
Remove-Item -LiteralPath .\logs, .\runs, .\fetch_outputs, .\stats.json -Recurse -Force -ErrorAction SilentlyContinue
```

Only run destructive cleanup commands inside the repository root after checking
the current path.
