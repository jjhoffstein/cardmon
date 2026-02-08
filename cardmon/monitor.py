import asyncio, logging, json, re
from .models import CheckResult, Schumer, Benefits
from .repository import CardRepository
from .fetcher import CardFetcher
from .extractors import get_extractor

log = logging.getLogger(__name__)

class BenefitsExtractor:
    def __init__(self, api_key: str): self.api_key = api_key

    def _prepare_content(self, content: str, max_tokens: int = 12000) -> str:
        import tiktoken
        enc = tiktoken.encoding_for_model('gpt-4')
        skip = ['update your browser', 'cookie', 'privacy', 'footer', 'menu', 'log in', 'sign in']
        keep = ['reward', 'benefit', 'earn', 'point', 'mile', 'fee', 'rate', 'credit', 'bonus', 'travel', 'lounge', 'bag', 'status', 'welcome', 'annual']
        sections = re.split(r'\n(?=##?\s)', content)
        relevant = [s for s in sections if any(k in s.lower() for k in keep) and not any(k in s.lower() for k in skip)]
        out = '\n'.join(relevant) if relevant else content
        tokens = enc.encode(out)
        if len(tokens) > max_tokens: out = enc.decode(tokens[:max_tokens])
        return out

    def extract(self, content: str) -> Benefits:
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        schema = json.dumps(Benefits.model_json_schema(), indent=2)
        prompt = f"Extract credit card benefits. Return ONLY valid JSON matching this schema:\n{schema}\n\nCONTENT:\n{self._prepare_content(content)}"
        resp = client.messages.create(model='claude-sonnet-4-20250514', max_tokens=3000, messages=[dict(role='user', content=prompt)])
        txt = resp.content[0].text
        if '```' in txt: txt = txt.split('```')[1].replace('json', '', 1).strip()
        return Benefits.model_validate_json(txt)

class CardMonitor:
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
            ext = get_extractor(card.issuer)
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

    async def notify(self, results: list, webhook_url: str, slack: bool = True):
        from .notifiers import get_notifier
        notifier = get_notifier(webhook_url, slack)
        await notifier.send(results)
    def notify(self, results: list, webhook_url: str, slack: bool = True):
        "Send notification for changed cards to webhook (Slack or generic)"
        import httpx
        changed = [r for r in results if r.changed]
        if not changed: return
        if slack:
            payload = dict(text=f"🃏 Card changes detected: {', '.join(r.name for r in changed)}", blocks=[dict(type="section", text=dict(type="mrkdwn", text="*Card changes detected:*\n" + "\n".join(f"• {r.name}: fee={r.schumer.annual_fee if r.schumer else '?'}" for r in changed)))])
        else:
            payload = dict(event="card_change", cards=[dict(name=r.name, annual_fee=r.schumer.annual_fee if r.schumer else None) for r in changed])
        httpx.post(webhook_url, json=payload)

