from bs4 import BeautifulSoup
from ..models import Schumer
from .base import BaseSchumerExtractor

class AmexExtractor(BaseSchumerExtractor):
    def parse(self, soup: BeautifulSoup) -> Schumer:
        data = {}
        for row in soup.select('tr, [class*="rate"], [class*="fee"]'):
            txt = row.get_text(' ', strip=True).lower()
            val = row.get_text(' ', strip=True)
            if 'purchase' in txt and 'apr' in txt: data['purchase_apr'] = val
            elif 'annual' in txt and 'fee' in txt: data['annual_fee'] = val
            elif 'foreign' in txt: data['foreign_tx_fee'] = val
            elif 'late' in txt: data['late_fee'] = val
        return Schumer(**data)
