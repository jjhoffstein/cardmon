import httpx
from .base import BaseNotifier

class WebhookNotifier(BaseNotifier):
    def __init__(self, webhook_url: str): self.webhook_url = webhook_url

    async def send(self, results: list) -> None:
        changed = [r for r in results if r.changed]
        if not changed: return
        payload = dict(event="card_change", cards=[dict(name=r.name, changed=r.changed, annual_fee=r.schumer.annual_fee if r.schumer else None) for r in changed])
        async with httpx.AsyncClient() as client: await client.post(self.webhook_url, json=payload)
