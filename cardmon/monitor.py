import asyncio, logging
from .models import CheckResult, Schumer
from .repository import CardRepository
from .fetcher import CardFetcher
from .extractors import SchumerExtractor, BenefitsExtractor

log = logging.getLogger(__name__)

class CardMonitor:
    "Orchestrates card monitoring pipeline"
    def __init__(self, db_path: str = 'cardmon.db', api_key: str|None = None):
        self.repo = CardRepository(db_path)
        self.api_key = api_key

    async def check_card(self, name: str) -> CheckResult:
        card = self.repo.get_card(name)
        if not card: return CheckResult(name=name, changed=False, error='Card not found')
        async with CardFetcher() as f:
            content, err = await f.fetch(card.url, card.selector)
            if err: return CheckResult(name=name, changed=False, error=err)
            h = f.hash(content)
            last = self.repo.last_check(name)
            changed = not last or last['hash'] != h
            diff_text = f.diff(last['content'] if last else '', content) if changed else None
            ext = SchumerExtractor()
            tcs = card.tcs_url or await ext.find_tcs_url(f.client, card.url)
            schumer, _ = await ext.extract(f.client, tcs) if tcs else (Schumer(), None)
            benefits = None
            if changed and self.api_key:
                try: benefits = BenefitsExtractor(self.api_key).extract(content)
                except Exception as e: log.error(f"Benefits extraction failed for {name}: {e}")
            self.repo.save_check(name, h, content, schumer, benefits)
            if changed: self.repo.queue_add(name); log.info(f"{name} changed")
            return CheckResult(name=name, changed=changed, schumer=schumer, benefits=benefits, diff=diff_text)

    async def check_all(self, issuer: str|None = None) -> list[CheckResult]:
        cards = self.repo.get_cards(issuer)
        return await asyncio.gather(*[self.check_card(c.name) for c in cards])
