# Fresh-Checkout Setup Verification

This document records a clean verification pass from a fresh clone of the
public GitHub repository. It is intended to give maintainers and reviewers a
quick reproducibility signal.

## Verification Summary

- Date: 2026-05-31
- Platform: Windows / PowerShell
- Python: 3.13.7
- Repository: https://github.com/Kyo14363/telegram-codex-bridge
- Result: pass

## Commands Run

The repository was cloned into a temporary directory outside the development
checkout:

```powershell
git clone --depth 1 https://github.com/Kyo14363/telegram-codex-bridge.git
cd telegram-codex-bridge
python -m pip install -r requirements.txt
python -m compileall -q .
python smoke_tests.py
python -c "from config import CONFIG; print(CONFIG['WORKING_DIR'].is_absolute()); print(CONFIG['CODEX_FULL_AUTO'])"
```

## Results

| Step | Result | Notes |
|---|---|---|
| `git clone --depth 1` | pass | Fresh clone from GitHub completed. |
| `python -m pip install -r requirements.txt` | pass | Required packages were already installed in the verification environment. |
| `python -m compileall -q .` | pass | All Python files compiled. |
| `python smoke_tests.py` | pass | 7 tests passed. |
| `config` import without `.env` | pass | `WORKING_DIR` resolved to an absolute path and `CODEX_FULL_AUTO` defaulted to `False`. |

Smoke-test output:

```text
Ran 7 tests
OK
```

Config sanity output:

```text
True
False
```

## What This Verification Covers

- Public clone works.
- Runtime dependencies install.
- Python files compile.
- Smoke tests run without Telegram, network calls, or live Codex tasks.
- Configuration can import without a `.env` file.
- Safe default `TCB_CODEX_FULL_AUTO=false` remains intact.
- Relative runtime paths resolve to absolute paths.

## What This Verification Does Not Cover

- A live Telegram polling session from the fresh clone.
- A live Codex API/model call from the fresh clone.
- macOS or Linux setup.
- A new virtual environment with an empty package cache.

Live Telegram and Codex behavior is covered separately in
[DEMO_TRANSCRIPT.md](DEMO_TRANSCRIPT.md).

## Re-running This Check

Use a temporary directory and delete it after verification. Do not reuse a
working directory that contains `.env`, logs, runs, or private fetch outputs.
