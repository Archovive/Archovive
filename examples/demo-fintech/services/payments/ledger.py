"""Ledger — sensitive payment state."""

from shared.config import settings
from services.notifications.sender import notify_ops


def post_transaction(account_id: str, amount: float) -> dict:
    notify_ops(f"ledger.post {account_id} {amount}")
    return {"account_id": account_id, "amount": amount, "currency": settings.currency}
