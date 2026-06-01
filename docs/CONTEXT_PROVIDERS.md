# Context Providers

Telegram Codex Bridge currently includes built-in URL preprocessing for GitHub,
X/Twitter, YouTube, and general web pages. The v0.3 direction is to keep this
small and explicit rather than introducing a broad plugin system too early.

## Current Boundary

Context providers should:

- accept a URL or message fragment
- return bounded text context for one Codex task
- avoid writing private data outside configured runtime folders
- make failures visible without blocking the whole bridge when possible
- keep fetched content clearly separated from the maintainer's instruction

Context providers should not:

- execute arbitrary code from fetched pages
- silently expand filesystem access
- require hosted infrastructure
- turn the bridge into a crawler or background sync service

## Existing Provider Families

| Provider family | Purpose |
|---|---|
| GitHub repository links | Fetch public repository metadata and README-like context. |
| General web pages | Extract readable page text when possible. |
| YouTube links | Gather lightweight video metadata/transcript context when available. |
| X/Twitter links | Attempt useful text extraction while tolerating dynamic-page limits. |

## Minimal Future Interface

A future provider registry should stay close to this shape:

```text
detect(message) -> matched URLs or fragments
fetch(match, config, metrics) -> context text plus short status
```

The bridge should continue to build one final Codex prompt from:

- the original Telegram message
- runtime guidance
- fetched context
- a clear note that fetched content is untrusted

## v0.3 Scope

For v0.3, the useful step is documentation and tests around provider behavior,
not a large plugin framework. A code-level registry can wait until there are
multiple external contributors or a concrete provider that does not fit the
current module.
