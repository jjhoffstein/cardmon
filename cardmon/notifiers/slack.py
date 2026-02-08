import httpx
from .base import BaseNotifier

class SlackNotifier(BaseNotifier):
    def __init__(self, webhook_url: str): self.webhook_url = webhook_url

    async def send(self, results: list) -> None:
        changed = [r for r in results if r.changed]
        if not changed: return
        blocks = [dict(type="section", text=dict(type="mrkdwn", text="*Card changes detected:*\n" + "\n".join(f"• {r.name}: fee={r.schumer.annual_fee if r.schumer else '?'}" for r in changed)))]
        payload = dict(text=f"🃏 {len(changed)} card(s) changed", blocks=blocks)
        async with httpx.AsyncClient() as client: await client.post(self.webhook_url, json=payload)
