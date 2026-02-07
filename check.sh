#!/bin/bash
set -e
echo "Running ruff..."
ruff check cardmon/
echo "Running tests..."
pytest tests/ -v
echo "All checks passed!"
