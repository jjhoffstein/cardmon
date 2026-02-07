import pytest
from pathlib import Path
from bs4 import BeautifulSoup
from cardmon.models import Schumer, Benefits
from cardmon.extractors import get_extractor

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
    ext = get_extractor('barclays')
    s = ext.parse(soup)
    assert s.annual_fee == '$0'

def test_get_extractor_returns_correct_type():
    assert get_extractor('chase').__class__.__name__ == 'ChaseExtractor'
    assert get_extractor('barclays').__class__.__name__ == 'BarclaysExtractor'
    assert get_extractor('unknown').__class__.__name__ == 'BarclaysExtractor'
