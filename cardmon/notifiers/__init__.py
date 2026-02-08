from .base import BaseNotifier
from .slack import SlackNotifier
from .webhook import WebhookNotifier

def get_notifier(webhook_url: str, slack: bool = True) -> BaseNotifier:
    return SlackNotifier(webhook_url) if slack else WebhookNotifier(webhook_url)

__all__ = ['BaseNotifier', 'SlackNotifier', 'WebhookNotifier', 'get_notifier']
