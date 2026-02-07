from abc import ABC
from bs4 import BeautifulSoup
from ..models import Schumer

class BaseSchumerExtractor(ABC):
    "Base class for issuer-specific Schumer extractors"

    label_map = dict(
        purchase_apr=['purchase', 'apr'],
        balance_transfer_apr=['balance transfer', 'apr'],
        cash_advance_apr=['cash advance', 'apr'],
        annual_fee=['annual', 'fee'],
        foreign_tx_fee=['foreign'],
        late_fee=['late'],
    )

    def parse(self, soup: BeautifulSoup) -> Schumer:
        data = {}
        for row in soup.select(self.row_selector):
            cells = row.find_all(self.cell_tags)
            if len(cells) < 2: continue
            label, val = cells[0].get_text(' ', strip=True).lower(), cells[1].get_text(' ', strip=True)
            for field, keywords in self.label_map.items():
                if all(k in label for k in keywords) and field not in data: data[field] = val; break
        return Schumer(**data)

    @property
    def row_selector(self): return 'tr'

    @property
    def cell_tags(self): return ['td', 'th']

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
