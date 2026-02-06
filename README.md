# cardmon

[![CI](https://github.com/yourusername/cardmon/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/cardmon/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Credit card benefits monitoring system. Track changes to card terms, rewards, and benefits across multiple issuers.

## Features

- **Change detection** - Hash-based monitoring, only alerts when content changes
- **Schumer box extraction** - Structured parsing of APRs, fees from official T&Cs
- **LLM benefits extraction** - Optional AI-powered extraction of rewards, perks
- **Multi-issuer support** - Plugin architecture for issuer-specific parsing
- **Review queue** - Human-in-the-loop approval for financial accuracy

## Quick Start

    pip install cardmon

    # Add cards via config
    cat > cards.yaml << EOF
    cards:
      chase:
        - name: Sapphire Preferred
          url: https://creditcards.chase.com/rewards-credit-cards/sapphire/preferred
          tcs_url: https://sites.chase.com/services/creatives/pricingandterms.html/content/dam/pricingandterms/LGC61729.html
    EOF

    cardmon sync
    cardmon check

## CLI Commands

    cardmon add <name> <url> <issuer>   # Add a card
    cardmon ls                          # List cards
    cardmon sync                        # Sync from cards.yaml
    cardmon check [--name X] [--issuer Y]  # Check for changes
    cardmon queue                       # View review queue
    cardmon approve <id>                # Approve reviewed item

## Configuration

Cards are defined in `cards.yaml`, grouped by issuer:

    cards:
      chase:
        - name: Sapphire Reserve
          url: https://creditcards.chase.com/...
          tcs_url: https://sites.chase.com/...  # Explicit T&C URL

## Environment Variables

- `ANTHROPIC_API_KEY` - Required for LLM benefits extraction (optional feature)

## Development

    git clone https://github.com/yourusername/cardmon.git
    cd cardmon
    pip install -e ".[dev]"
    pytest tests/ -v

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT
