# Changelog

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
