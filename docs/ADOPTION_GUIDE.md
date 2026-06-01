# Adoption Guide

This guide is for maintainers who want to decide whether Telegram Codex Bridge
is worth trying in their own workflow.

## What To Try First

Start with review-only mode. The goal is to verify the control loop before
allowing file edits or unattended commands.

```env
TCB_CODEX_FULL_AUTO=false
TCB_CODEX_SEARCH=false
TCB_WORKING_DIR=.\workspace
TCB_CODEX_EXTRA_DIRS=
```

Good first tasks:

- triage a public issue URL
- summarize whether a public repository is relevant
- prepare a release checklist from a disposable checkout
- draft a maintainer reply from a pasted user report

Avoid first-run tasks that involve secrets, private repositories, production
workspaces, or destructive commands.

## Evaluation Checklist

The bridge is probably useful for you if:

- you already use Telegram for maintainer notifications
- you can run Codex CLI locally on a machine you control
- you want bounded, reviewable maintainer tasks rather than a hosted bot
- you are comfortable reviewing AI output before acting on it
- your tasks fit one-message workflows such as triage, review, checklist, or
  diagnostic summary

The bridge is probably not a fit if:

- you need a hosted SaaS service
- you need multi-user tenant management
- you cannot keep a Telegram bot token private
- you want Codex to run without a local Codex CLI installation
- you need unattended production automation from day one

## Suggested Trial Plan

1. Clone the repository and install dependencies.
2. Create a dedicated Telegram bot for the bridge.
3. Set `TCB_ALLOWED_USER_IDS` before starting the bridge.
4. Run `/status` from Telegram and confirm `full auto: off`.
5. Send one issue-triage prompt from [Prompt templates](PROMPT_TEMPLATES.md).
6. Review `logs/`, `runs/`, and the Telegram result for private data.
7. Decide whether to keep using review-only mode or point the bridge at a
   disposable local checkout.

## Adoption Signals

A successful trial should produce:

- a clear Telegram response
- no unexpected local file changes
- a bounded result that can be pasted into a maintainer workflow
- runtime files that are understandable and easy to redact
- a repeatable command path through CI or local verification

## Do Not Skip

- Keep `.env` out of git.
- Keep `TCB_ALLOWED_USER_IDS` explicit.
- Keep `TCB_CODEX_FULL_AUTO=false` until you intentionally test edit-capable
  workflows.
- Use one dedicated working directory per task family.
- Read [Deployment security checklist](DEPLOYMENT_SECURITY_CHECKLIST.md) before
  using the bridge on a real repository.
