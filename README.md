# cardmon

[![CI](https://github.com/jjhoffstein/cardmon/actions/workflows/ci.yml/badge.svg)](https://github.com/jjhoffstein/cardmon/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Monitor credit card benefits, rewards, and terms. Detects changes to card marketing pages and extracts structured data from official Terms & Conditions.

## Why?

Credit card issuers frequently change benefits, bonuses, and fees. This tool:
- Monitors card pages for changes (hash-based, cost-efficient)
- Extracts Schumer box data (APRs, fees) from official T&Cs
- Optionally uses AI to extract benefits and restrictions
- Queues changes for human review (important for financial accuracy)

## Installation

    pip install -e .

## Quick Start

1. Create a `cards.yaml` config (see `cards.yaml` for full example)
2. Run `cardmon sync && cardmon check`

## CLI Reference

| Command | Description |
|---------|-------------|
| `cardmon add <name> <url> <issuer>` | Add a single card |
| `cardmon ls [--issuer X]` | List monitored cards |
| `cardmon sync` | Sync cards from cards.yaml |
| `cardmon check [--name X] [--issuer Y]` | Check for changes |
| `cardmon queue` | View pending reviews |
| `cardmon approve <id>` | Mark item as reviewed |

## Configuration

Cards grouped by issuer in `cards.yaml`:

    cards:
      chase:
        - name: Sapphire Reserve
          url: https://creditcards.chase.com/...
          tcs_url: https://sites.chase.com/...  # Required if T&Cs load via JS

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | No | Enables AI-powered benefits extraction |

## Architecture

    cardmon/
    ├── extractors/       # Issuer-specific parsers (plugin architecture)
    │   ├── base.py       # Shared parsing logic
    │   └── chase.py      # Issuer overrides (label_map, selectors)
    ├── models.py         # Pydantic schemas
    ├── repository.py     # SQLite storage
    ├── fetcher.py        # Async HTTP client
    ├── monitor.py        # Orchestration
    └── cli.py            # Typer CLI

## Development

    git clone https://github.com/jjhoffstein/cardmon.git
    cd cardmon
    pip install -e ".[dev]"
    ./check.sh              # Run linting + tests

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
