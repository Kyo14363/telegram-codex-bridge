# Platform Setup Notes

Telegram Codex Bridge is a Python application that shells out to Codex CLI.
The same core workflow should work across platforms, but live Telegram
dogfooding has primarily been performed on Windows so far.

GitHub Actions runs basic install, lint, compile, smoke, sanity, and package
build checks on Windows, macOS, and Linux. That CI coverage is not the same as a
live Telegram polling test on every platform.

## Shared Requirements

- Python 3.11 or newer
- Codex CLI available in `PATH`
- a Telegram bot token from BotFather
- your Telegram numeric user ID for `TCB_ALLOWED_USER_IDS`
- network access to Telegram and any URLs you ask the bridge to fetch

## Windows

Windows is the current dogfooded platform.

```powershell
git clone https://github.com/Kyo14363/telegram-codex-bridge.git
cd telegram-codex-bridge
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python telegram_bridge_codex.py
```

Optional development install:

```powershell
python -m pip install -e ".[dev]"
python -m ruff check .
python smoke_tests.py
python scripts\sanity_check.py
```

Notes:

- `start_bridge.bat` is provided for convenience.
- Avoid running two bridge instances with the same Telegram bot token, because
  Telegram polling can conflict.
- PowerShell may display successful unittest output as `NativeCommandError`
  when stderr is captured. Check the final `OK` and process exit code.

## macOS

Basic CI checks run on macOS. Live Telegram polling still needs more public
dogfooding evidence.

```bash
git clone https://github.com/Kyo14363/telegram-codex-bridge.git
cd telegram-codex-bridge
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 telegram_bridge_codex.py
```

Use `python3 -m pip install -e ".[dev]"` for development checks.

## Linux

Basic CI checks run on Linux. Live Telegram polling still needs more public
dogfooding evidence.

```bash
git clone https://github.com/Kyo14363/telegram-codex-bridge.git
cd telegram-codex-bridge
python3 -m pip install -r requirements.txt
cp .env.example .env
python3 telegram_bridge_codex.py
```

For long-running use, prefer a user-level service manager such as `systemd`
after you have completed a manual review-only test.

## Verification Commands

Run these before trusting a checkout:

```bash
python -m pip install -e ".[dev]"
python -m ruff check .
python -m compileall -q .
python smoke_tests.py
python scripts/sanity_check.py
python -m build
```

On Windows, replace `python` with your Python launcher if needed.

## Current Coverage

| Platform | CI install/test/build | Live Telegram dogfooding |
|---|---:|---:|
| Windows | Yes | Yes |
| macOS | Yes | Not yet documented |
| Linux | Yes | Not yet documented |
