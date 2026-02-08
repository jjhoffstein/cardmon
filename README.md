# cardmon

[![CI](https://github.com/jjhoffstein/cardmon/actions/workflows/ci.yml/badge.svg)](https://github.com/jjhoffstein/cardmon/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Monitor credit card terms and benefits for changes.

## What It Does

- Checks card marketing pages for changes (hash-based)
- Extracts Schumer box data (APRs, fees) from Terms & Conditions pages
- Queues changes for human review
- Sends Slack/webhook notifications when changes detected
- Optionally uses Claude API to extract benefits (experimental)

## Limitations

- **JS-rendered pages**: Amex, Citi, Capital One T&Cs often load via JavaScript — extraction may fail without explicit `tcs_url`
- **Not real-time**: Designed for daily/weekly batch checks
- **Manual T&C URL discovery**: Some cards require manually finding the T&C URL
- **No retry logic yet**: Transient failures are not retried

## Installation

    pip install -e .

## Quick Start

    cardmon sync           # Load cards from cards.yaml
    cardmon check          # Check all cards
    cardmon queue          # View changes pending review
    cardmon approve 1      # Mark reviewed

## CLI

| Command | Description |
|---------|-------------|
| `cardmon sync` | Load cards from cards.yaml |
| `cardmon check [--issuer X] [--webhook URL]` | Check for changes |
| `cardmon ls` | List cards |
| `cardmon queue` | Pending reviews |
| `cardmon approve <id>` | Mark reviewed |
| `cardmon history <name>` | Check history for a card |

## Configuration

`cards.yaml`:

    cards:
      chase:
        - name: Sapphire Reserve
          url: https://creditcards.chase.com/...
          tcs_url: https://sites.chase.com/...  # Often required

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | No | Enables AI benefits extraction |

## Architecture

    cardmon/
    ├── extractors/       # Per-issuer HTML parsing (plugin)
    ├── notifiers/        # Slack, webhook (plugin)
    ├── models.py         # Pydantic schemas
    ├── repository.py     # SQLite
    ├── fetcher.py        # Async HTTP
    ├── monitor.py        # Orchestration
    └── cli.py            # CLI

## Extending

- **New issuer**: Subclass `BaseSchumerExtractor` in `extractors/`
- **New notifier**: Subclass `BaseNotifier` in `notifiers/`

See [AGENTS.md](AGENTS.md) for AI-assisted development guidance.

## Development

    pip install -e ".[dev]"
    ./check.sh

## Status

Early-stage project. Works for Barclays and Chase cards. Other issuers partially supported.

## License

MIT
