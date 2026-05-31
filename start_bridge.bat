@echo off
setlocal

cd /d "%~dp0"

if not exist ".env" (
    echo [Warning] .env was not found. Copy .env.example to .env and fill it in.
)

where python >nul 2>nul
if errorlevel 1 (
    echo [Error] python was not found in PATH.
    exit /b 1
)

where codex >nul 2>nul
if errorlevel 1 (
    echo [Error] codex CLI was not found in PATH.
    exit /b 1
)

python -m pip install -r requirements.txt
if errorlevel 1 (
    echo [Error] dependency installation failed.
    exit /b 1
)

python telegram_bridge_codex.py
