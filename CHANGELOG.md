# Changelog

## Unreleased

- Added adoption, platform setup, deployment security checklist, and context
  provider boundary docs for v0.3 preparation.
- Reworked the live workflow runbook into OpenAI-facing dogfooding evidence and
  application framing.
- Fixed Windows-style relative path settings such as `.\workspace` on macOS and
  Linux.
- Expanded CI to run install, lint, compile, smoke, sanity, and package build
  checks across Windows, macOS, and Linux.
- Further redacted the demo transcript by replacing the local model override
  value with a placeholder.

## 0.2.1 - Dogfooding evidence refresh

- Added a redacted live release-checklist transcript from Telegram dogfooding.
- Added a redacted live repository-context-review transcript from Telegram
  dogfooding.
- Reworked the demo transcript into a cleaner public-facing evidence page.
- Added a redacted live issue-triage transcript from Telegram dogfooding.
- Added a live workflow runbook for Telegram dogfooding, transcript capture,
  and public redaction.
- Created a public dogfooding issue for the issue-triage workflow.
- Refreshed setup verification and roadmap docs after dogfooding found stale
  entries.
- Added package build verification to CI and development dependencies.

## 0.2.0 - Maintainer workflow kit

- Added Python project metadata in `pyproject.toml`, including an editable
  install path, optional dependency groups, Ruff settings, and a console script.
- Added maintainer prompt templates for issue triage, PR review, release
  checklists, CI failure triage, and repository context review.
- Added workflow presets for review-only, URL context, local maintainer, and
  scoped full-auto modes.
- Expanded smoke tests for output formatting, stderr noise filtering, and
  prompt template coverage.
- Extended repository sanity checks to scan TOML files and verify
  `pyproject.toml` version consistency.
- Updated CI to install the editable package and use the checked-in Ruff config.

## 0.1.3 - CI hardening

- Added development requirements for CI-only tooling.
- Added high-signal Ruff linting for syntax and undefined-name errors.
- Added repository sanity checks for tracked runtime artifacts, private path
  leaks, token patterns, internal Markdown links, and version consistency.
- Split the GitHub Actions workflow into clearer install, lint, compile, smoke,
  and sanity stages.

## 0.1.2 - Setup verification and troubleshooting

- Added fresh-checkout setup verification documentation.
- Added troubleshooting documentation based on real dogfooding failures.
- Linked setup verification and troubleshooting docs from the README.

## 0.1.1 - Live dry-run hardening

- Added a redacted live Telegram dry-run transcript.
- Documented the two dry-run fixes discovered while dogfooding: repo-root
  relative path resolution and explicit Codex model compatibility settings.

## 0.1.0 - Public OSS readiness release

- Added public-safe Telegram Codex Bridge entry point.
- Split configuration, metrics, Codex runner, and Telegram handlers into
  focused modules.
- Added `.env.example`, `.gitignore`, MIT license, setup docs, command docs,
  smoke tests, and GitHub Actions compile checks.
- Defaulted runtime paths to repo-local folders and kept `--full-auto` opt-in.
- Added maintainer workflow, security, roadmap, and demo transcript docs.
- Added GitHub issue templates for bugs, feature requests, and workflow
  examples, plus a pull request template and contribution guide.
- Expanded smoke tests around command safety defaults, authorization, prompt
  construction, and Codex event summaries.
