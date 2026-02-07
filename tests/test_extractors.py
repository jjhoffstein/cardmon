import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from cardmon.models import Schumer, Benefits
from cardmon.extractors import SchumerExtractor

FIXTURES = Path(__file__).parent / 'fixtures'

def test_schumer_model():
    s = Schumer(annual_fee='$99', purchase_apr='19.99%')
    assert s.annual_fee == '$99'
    assert s.purchase_apr == '19.99%'
    assert s.foreign_tx_fee is None

def test_benefits_model():
    b = Benefits(bonus_points=50000, bonus_spend_required=3000, bonus_time_limit='90 days')
    assert b.bonus_points == 50000
    assert b.spend_multipliers == []

def test_schumer_extraction_from_fixture():
    html = (FIXTURES / 'jetblue.html').read_text()
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    for row in soup.select('tr'):
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2: continue
        label, val = cells[0].get_text(' ', strip=True).lower(), cells[1].get_text(' ', strip=True)
        if 'annual fee' in label: data['annual_fee'] = val
    s = Schumer(**data)
    assert s.annual_fee == '$0'
