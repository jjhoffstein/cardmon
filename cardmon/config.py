import yaml, re
from pathlib import Path
from .models import Card
from .repository import CardRepository

def slugify(name: str) -> str: return re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')

def load_cards(config_path: str|Path = 'cards.yaml') -> list[Card]:
    "Load card definitions from grouped YAML config"
    p = Path(config_path)
    if not p.exists(): return []
    data = yaml.safe_load(p.read_text())
    cards = []
    for issuer, items in data.get('cards', {}).items():
        for c in items:
            cards.append(Card(name=slugify(c['name']), url=c['url'], issuer=issuer, selector=c.get('selector'), tcs_url=c.get('tcs_url')))
    return cards

def sync_cards(config_path: str|Path = 'cards.yaml', db_path: str = 'cardmon.db'):
    "Sync cards from config file to database"
    repo = CardRepository(db_path)
    cards = load_cards(config_path)
    for c in cards: repo.add_card(c)
    return cards
