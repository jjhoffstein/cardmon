import hashlib, difflib, asyncio
import httpx
from bs4 import BeautifulSoup
import html2text

_hdrs = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
_h2t = html2text.HTML2Text()
_h2t.ignore_links, _h2t.ignore_images, _h2t.body_width = False, False, 0

class CardFetcher:
    "Async HTTP fetching with hash, diff, and rate limiting"
    def __init__(self, timeout: int = 30, max_concurrent: int = 3, delay: float = 0.5):
        self.timeout, self.delay, self.client = timeout, delay, None
        self._sem = asyncio.Semaphore(max_concurrent)

    async def __aenter__(self):
        self.client = httpx.AsyncClient(follow_redirects=True, headers=_hdrs, timeout=self.timeout)
        return self

    async def __aexit__(self, *args): await self.client.aclose()

    async def fetch(self, url: str, selector: str|None = None) -> tuple[str|None, str|None]:
        async with self._sem:
            if self.delay: await asyncio.sleep(self.delay)
            try:
                r = await self.client.get(url)
                soup = BeautifulSoup(r.text, 'lxml')
                if selector: soup = soup.select_one(selector) or soup
                return _h2t.handle(str(soup)).strip(), None
            except Exception as e: return None, str(e)

    async def fetch_html(self, url: str) -> tuple[BeautifulSoup|None, str|None]:
        async with self._sem:
            if self.delay: await asyncio.sleep(self.delay)
            try:
                r = await self.client.get(url)
                return BeautifulSoup(r.text, 'lxml'), None
            except Exception as e: return None, str(e)

    def hash(self, content: str) -> str: return hashlib.sha256(content.encode()).hexdigest()[:16]

    def diff(self, old: str|None, new: str) -> str:
        return '\n'.join(difflib.unified_diff((old or '').split('\n'), new.split('\n'), lineterm='', n=2))
