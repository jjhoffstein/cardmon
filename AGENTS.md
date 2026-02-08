# AGENTS.md

> Instructions for AI agents working on this codebase.

## Project Overview

**cardmon** monitors credit card marketing pages for changes and extracts structured data from Terms & Conditions. Uses plugin architectures for both issuer-specific parsing and notifications.

## Status

Early-stage. Works well for Barclays and Chase. Other issuers (Amex, Citi, Capital One) partially supported — their T&C pages often require JavaScript rendering.

## File Map

| File | Purpose |
|------|---------|
| `models.py` | Pydantic schemas: Schumer, Benefits, Card, CheckResult |
| `repository.py` | SQLite: cards, checks, queue tables |
| `fetcher.py` | Async HTTP with rate limiting (1s delay), hash, diff |
| `monitor.py` | Orchestrator + BenefitsExtractor (LLM) |
| `config.py` | YAML loader for cards.yaml |
| `cli.py` | Typer CLI: sync, check, ls, queue, approve, history |
| `extractors/` | Per-issuer Schumer parsing (plugin) |
| `notifiers/` | Slack, webhook notifications (plugin) |

## Data Flow

    cards.yaml -> sync -> SQLite
    check -> fetch -> hash -> changed? -> extract Schumer -> save -> queue -> notify

## Common Tasks

### Add a new issuer

1. Create `extractors/{issuer}.py` subclassing `BaseSchumerExtractor`
2. Override `label_map`, `row_selector`, or `cell_tags` as needed
3. Register in `extractors/__init__.py`
4. Save fixture: `tests/fixtures/{issuer}.html`
5. Add test in `tests/test_extractors.py`

### Add a new notifier

1. Create `notifiers/{service}.py` subclassing `BaseNotifier`
2. Implement `async def send(self, results) -> None`
3. Register in `notifiers/__init__.py`

### Add a new card

Edit `cards.yaml`. Include `tcs_url` if T&Cs load via JavaScript.

### Fix "Schumer = None"

1. Check if T&C URL returns 403/404
2. Inspect HTML — may need custom `label_map` or `row_selector`
3. If JS-rendered, find explicit T&C URL and add to config

## Testing

    ./check.sh

## Known Limitations

- No retry logic for transient failures
- No concurrency limit (could hammer servers)
- Amex/Citi/Capital One T&Cs often JS-rendered
- BenefitsExtractor (LLM) is experimental

## Code Style

- Type hints on all signatures
- Pydantic for data models
- Async for HTTP operations
- Single-line conditionals/loops where readable
- No inline comments
