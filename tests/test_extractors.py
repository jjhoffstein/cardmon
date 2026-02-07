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

def test_barclays_extractor():
    soup = BeautifulSoup((FIXTURES / 'jetblue.html').read_text(), 'lxml')
    s = get_extractor('barclays').parse(soup)
    assert s.annual_fee == '$0'

def test_chase_extractor():
    soup = BeautifulSoup((FIXTURES / 'chase.html').read_text(), 'lxml')
    s = get_extractor('chase').parse(soup)
    assert s.annual_fee is not None
    assert '$' in s.annual_fee or 'None' in s.annual_fee

def test_get_extractor_returns_correct_type():
    assert get_extractor('chase').__class__.__name__ == 'ChaseExtractor'
    assert get_extractor('barclays').__class__.__name__ == 'BarclaysExtractor'
    assert get_extractor('amex').__class__.__name__ == 'AmexExtractor'
    assert get_extractor('citi').__class__.__name__ == 'CitiExtractor'
    assert get_extractor('capital_one').__class__.__name__ == 'CapitalOneExtractor'
    assert get_extractor('unknown').__class__.__name__ == 'BarclaysExtractor'
