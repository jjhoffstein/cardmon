# AGENTS.md

> Instructions for AI agents working on this codebase.

## Project Overview

**cardmon** monitors credit card marketing pages for changes and extracts structured data from Terms & Conditions. It uses a plugin architecture for issuer-specific parsing.

## File Map

| File | Purpose |
|------|---------|
| `cardmon/extractors/base.py` | Base extractor with shared parse() logic |
| `cardmon/extractors/{issuer}.py` | Issuer-specific overrides |
| `cardmon/models.py` | Pydantic schemas |
| `cardmon/repository.py` | SQLite CRUD |
| `cardmon/fetcher.py` | Async HTTP with hash/diff |
| `cardmon/monitor.py` | Orchestration |
| `cardmon/cli.py` | Typer CLI |
| `cardmon/config.py` | YAML config loader |

## Common Tasks

### Add a new issuer

1. Create `cardmon/extractors/{issuer}.py` subclassing `BaseSchumerExtractor`
2. Override `label_map`, `row_selector`, or `cell_tags` as needed
3. Register in `cardmon/extractors/__init__.py`
4. Add fixture: `tests/fixtures/{issuer}.html`
5. Add test in `tests/test_extractors.py`

### Add a new card

Edit `cards.yaml`. Include `tcs_url` if T&Cs load via JavaScript.

### Fix extraction failures

- 403/404: May need different headers or URL
- Schumer=None: Check HTML structure, update `label_map` or selectors
- T&C not found: Add explicit `tcs_url` in config

## Testing

    ./check.sh

## Code Style

- Type hints required
- Pydantic for data models
- Async for HTTP
- No comments (docstrings for public APIs only)
