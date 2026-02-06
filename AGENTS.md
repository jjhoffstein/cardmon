# Agent Instructions for cardmon

## Project Context

This is a credit card benefits monitoring tool. It tracks changes to card marketing pages and extracts structured data from Terms & Conditions.

## When Working on This Codebase

### Adding a New Issuer

1. Create `cardmon/extractors/{issuer}.py`
2. Subclass `BaseSchumerExtractor`, implement `parse(soup) -> Schumer`
3. Add to `_EXTRACTORS` dict in `cardmon/extractors/__init__.py`
4. Add test fixture HTML in `tests/fixtures/`
5. Add test in `tests/test_extractors.py`

### Adding a New Card

Edit `cards.yaml` under the appropriate issuer. Include `tcs_url` if the page uses JavaScript to load T&Cs.

### Common Issues

- **403 errors**: Some issuers block requests. May need to add delays or different headers.
- **Schumer = None**: T&C page structure differs from extractor. Check the HTML, update parser.
- **T&C not found**: Page loads T&Cs via JS. Add explicit `tcs_url` in config.

### Testing

    pytest tests/ -v

### Code Style

- Type hints required
- Pydantic for data models
- Async for HTTP operations
- No comments in code - use docstrings for public functions only
