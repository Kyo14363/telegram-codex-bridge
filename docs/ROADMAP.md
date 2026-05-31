# Roadmap

This roadmap is intentionally small and maintainer-oriented. The project should
earn maturity through safer defaults, clearer workflows, and real dogfooding
before adding broad features.

## v0.1.x: Public Skeleton Hardening

- [x] Public repository skeleton
- [x] README, command docs, license, env template
- [x] GitHub Actions compile and smoke checks
- [x] Maintainer workflow guide
- [x] Security policy and security guide
- [x] Illustrative demo transcript
- [x] Issue templates
- [x] Contribution guide
- [x] First prerelease tag and GitHub release
- [x] Redacted live Telegram transcript
- [x] Fresh-checkout setup verification
- [x] Troubleshooting guide

## v0.2: Maintainer Workflow Kit

- [ ] Prompt templates for issue triage, PR review, release checklists, and CI
      failure triage
- [ ] More tests for prompt construction, Codex event parsing, and URL
      preprocessing edge cases
- [ ] Demo screenshots or terminal captures
- [ ] Optional workflow presets for review-only vs full-auto mode
- [ ] Better setup notes for Windows, macOS, and Linux

## v0.3: Adoptable OSS Tool

- [ ] Versioned release notes and GitHub releases
- [ ] Real-world dogfooding examples
- [ ] Contributor guide
- [ ] Security hardening checklist by deployment mode
- [ ] Minimal plugin architecture for extra URL/context providers

## Non-Goals for Now

- Hosted SaaS operation
- Multi-user tenant management
- Replacing GitHub Actions or full CI systems
- Running Codex without a local Codex CLI installation
