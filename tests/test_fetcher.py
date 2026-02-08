import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from cardmon.fetcher import CardFetcher

@pytest.mark.asyncio
async def test_fetcher_has_rate_limit_params():
    async with CardFetcher() as f:
        assert f.delay == 0.5
        assert f._sem._value == 3

@pytest.mark.asyncio
async def test_fetcher_custom_rate_limit():
    async with CardFetcher(max_concurrent=5, delay=1.0) as f:
        assert f.delay == 1.0
        assert f._sem._value == 5

@pytest.mark.asyncio
async def test_fetcher_semaphore_limits_concurrency():
    async with CardFetcher(max_concurrent=2, delay=0) as f:
        assert f._sem._value == 2
        async with f._sem: assert f._sem._value == 1
        assert f._sem._value == 2

@pytest.mark.asyncio
async def test_fetcher_fetch_returns_content():
    async with CardFetcher(delay=0) as f:
        mock_response = MagicMock()
        mock_response.text = '<html><body>Hello World</body></html>'
        f.client.get = AsyncMock(return_value=mock_response)
        content, err = await f.fetch('https://example.com')
        assert err is None
        assert 'Hello World' in content

@pytest.mark.asyncio
async def test_fetcher_fetch_handles_error():
    async with CardFetcher(delay=0) as f:
        f.client.get = AsyncMock(side_effect=Exception('Network error'))
        content, err = await f.fetch('https://example.com')
        assert content is None
        assert 'Network error' in err

@pytest.mark.asyncio
async def test_fetcher_hash_deterministic():
    f = CardFetcher()
    assert f.hash('test') == f.hash('test')
    assert f.hash('test') != f.hash('test2')

@pytest.mark.asyncio
async def test_fetcher_diff():
    f = CardFetcher()
    diff = f.diff('line1\nline2', 'line1\nline3')
    assert '-line2' in diff
    assert '+line3' in diff
