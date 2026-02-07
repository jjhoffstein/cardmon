import pytest
import tempfile
from pathlib import Path
from cardmon.repository import CardRepository
from cardmon.models import Card, Schumer

def test_add_and_get_card():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        repo = CardRepository(f.name)
        card = Card(name='test_card', url='https://example.com', issuer='test')
        repo.add_card(card)
        result = repo.get_card('test_card')
        assert result.name == 'test_card'
        assert result.url == 'https://example.com'
        Path(f.name).unlink()

def test_get_cards_by_issuer():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        repo = CardRepository(f.name)
        repo.add_card(Card(name='card1', url='https://a.com', issuer='chase'))
        repo.add_card(Card(name='card2', url='https://b.com', issuer='chase'))
        repo.add_card(Card(name='card3', url='https://c.com', issuer='amex'))
        assert len(repo.get_cards('chase')) == 2
        assert len(repo.get_cards('amex')) == 1
        assert len(repo.get_cards()) == 3
        Path(f.name).unlink()

def test_save_and_retrieve_check():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        repo = CardRepository(f.name)
        repo.add_card(Card(name='test', url='https://example.com', issuer='test'))
        schumer = Schumer(annual_fee='$99')
        repo.save_check('test', 'abc123', 'content here', schumer, None)
        last = repo.last_check('test')
        assert last['hash'] == 'abc123'
        assert last['content'] == 'content here'
        Path(f.name).unlink()

def test_queue_operations():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        repo = CardRepository(f.name)
        repo.queue_add('card1')
        repo.queue_add('card2')
        queue = repo.queue_list()
        assert len(queue) == 2
        repo.queue_approve(queue[0]['id'])
        assert len(repo.queue_list()) == 1
        Path(f.name).unlink()
