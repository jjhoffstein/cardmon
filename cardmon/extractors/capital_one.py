from bs4 import BeautifulSoup
from ..models import Schumer
from .base import BaseSchumerExtractor

class CapitalOneExtractor(BaseSchumerExtractor):
    def parse(self, soup: BeautifulSoup) -> Schumer:
        data = {}
        for row in soup.select('tr'):
            cells = row.find_all(['td', 'th'])
            if len(cells) < 2: continue
            label, val = cells[0].get_text(' ', strip=True).lower(), cells[1].get_text(' ', strip=True)
            if 'purchase' in label and 'apr' in label: data['purchase_apr'] = val
            elif 'balance transfer' in label and 'apr' in label: data['balance_transfer_apr'] = val
            elif 'cash advance' in label and 'apr' in label: data['cash_advance_apr'] = val
            elif 'annual' in label and 'fee' in label: data['annual_fee'] = val
            elif 'foreign' in label: data['foreign_tx_fee'] = val
            elif 'late' in label: data['late_fee'] = val
        return Schumer(**data)
