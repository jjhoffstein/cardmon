# Contributing to cardmon

## Development Setup

    git clone https://github.com/yourusername/cardmon.git
    cd cardmon
    pip install -e ".[dev]"

## Running Tests

    pytest tests/ -v

## Adding a New Issuer Extractor

1. Create `cardmon/extractors/newissuer.py`
2. Implement `parse(soup) -> Schumer` method
3. Register in `cardmon/extractors/__init__.py`
4. Add test fixture in `tests/fixtures/`

## Adding Cards

Edit `cards.yaml` - group by issuer, include `tcs_url` where auto-detection fails.

## Code Style

- Use type hints
- Keep functions focused
- Run `ruff check .` before committing
