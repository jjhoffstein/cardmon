import sqlite3, json
from datetime import datetime
from pathlib import Path
from .models import Card, Schumer, Benefits

class CardRepository:
    "SQLite storage for card monitoring"
    def __init__(self, path: str|Path = 'cardmon.db'):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._init()

    def _init(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS cards (name TEXT PRIMARY KEY, url TEXT, issuer TEXT, selector TEXT, tcs_url TEXT);
            CREATE TABLE IF NOT EXISTS checks (id INTEGER PRIMARY KEY, name TEXT, ts TEXT, hash TEXT, content TEXT, schumer TEXT, benefits TEXT);
            CREATE TABLE IF NOT EXISTS queue (id INTEGER PRIMARY KEY, name TEXT, ts TEXT, reviewed INTEGER DEFAULT 0);
            CREATE INDEX IF NOT EXISTS idx_checks_name_ts ON checks(name, ts DESC);
        """)
        self.conn.commit()

    def add_card(self, card: Card):
        self.conn.execute("INSERT OR REPLACE INTO cards VALUES (?,?,?,?,?)", (card.name, card.url, card.issuer, card.selector, card.tcs_url))
        self.conn.commit()

    def get_card(self, name: str) -> Card|None:
        r = self.conn.execute("SELECT * FROM cards WHERE name=?", (name,)).fetchone()
        return Card(**dict(r)) if r else None

    def get_cards(self, issuer: str|None = None) -> list[Card]:
        q = "SELECT * FROM cards" + (" WHERE issuer=?" if issuer else "")
        rows = self.conn.execute(q, (issuer,) if issuer else ()).fetchall()
        return [Card(**dict(r)) for r in rows]

    def last_check(self, name: str) -> dict|None:
        r = self.conn.execute("SELECT * FROM checks WHERE name=? ORDER BY ts DESC LIMIT 1", (name,)).fetchone()
        return dict(r) if r else None

    def save_check(self, name: str, h: str, content: str, schumer: Schumer|None, benefits: Benefits|None):
        self.conn.execute("INSERT INTO checks (name,ts,hash,content,schumer,benefits) VALUES (?,?,?,?,?,?)",
            (name, datetime.now().isoformat(), h, content, schumer.model_dump_json() if schumer else None, benefits.model_dump_json() if benefits else None))
        self.conn.commit()

    def queue_add(self, name: str):
        self.conn.execute("INSERT INTO queue (name,ts) VALUES (?,?)", (name, datetime.now().isoformat()))
        self.conn.commit()

    def queue_list(self) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM queue WHERE reviewed=0 ORDER BY ts DESC")]

    def queue_approve(self, id: int):
        self.conn.execute("UPDATE queue SET reviewed=1 WHERE id=?", (id,))
        self.conn.commit()

    def history(self, name: str, limit: int = 10) -> list[dict]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM checks WHERE name=? ORDER BY ts DESC LIMIT ?", (name, limit))]
