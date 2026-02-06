from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from ..models import Schumer

class BaseSchumerExtractor(ABC):
    "Base class for issuer-specific Schumer extractors"
    @abstractmethod
    def parse(self, soup: BeautifulSoup) -> Schumer: pass

    async def find_tcs_url(self, client, url: str) -> str|None:
        try:
            r = await client.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            for a in soup.find_all('a', href=True):
                href, txt = a['href'], a.get_text(' ', strip=True).lower()
                if 'terms' in txt or 'pricing' in txt or 'tcs' in href.lower() or 'terms' in href.lower():
                    if href.startswith('http'): return href
                    base = f"{url.split('/')[0]}//{url.split('/')[2]}"
                    return base + href if href.startswith('/') else href
            return None
        except: return None

    async def extract(self, client, tcs_url: str) -> tuple[Schumer, str|None]:
        try:
            r = await client.get(tcs_url)
            soup = BeautifulSoup(r.text, 'lxml')
            return self.parse(soup), None
        except Exception as e: return Schumer(), str(e)
