# Security Policy

Telegram Codex Bridge is a self-hosted tool that can run Codex CLI on your
machine. The full security guide is in [docs/SECURITY.md](docs/SECURITY.md).

## Supported Versions

This project is pre-1.0. Security fixes target the latest `main` branch.

## Reporting a Vulnerability

Please do not post active tokens, exploit details, or private logs in a public
issue.

Use GitHub's private vulnerability reporting or security advisory flow if it is
enabled. If private reporting is unavailable, open a minimal public issue that
describes the affected area and asks for a private contact path.

## Baseline Safety

- Set `TCB_ALLOWED_USER_IDS`.
- Keep `.env` private.
- Use a dedicated `TCB_WORKING_DIR`.
- Leave `TCB_CODEX_FULL_AUTO=false` unless you intentionally want unattended
  local actions.
