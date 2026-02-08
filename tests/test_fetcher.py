import pytest
import asyncio
import time
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
async def test_fetcher_respects_semaphore():
    async with CardFetcher(max_concurrent=2, delay=0.1) as f:
        start = time.time()
        await asyncio.gather(*[f.fetch('https://httpbin.org/delay/0') for _ in range(4)])
        elapsed = time.time() - start
        assert elapsed >= 0.4, "Should take at least 0.4s with 4 requests, max 2 concurrent, 0.1s delay each"

@pytest.mark.asyncio
async def test_fetcher_zero_delay():
    async with CardFetcher(delay=0) as f:
        content, err = await f.fetch('https://httpbin.org/html')
        assert err is None
        assert content is not None

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
