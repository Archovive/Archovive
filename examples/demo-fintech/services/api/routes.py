"""HTTP routes — crosses boundary into payments.ledger (demo violation)."""

from services.payments.ledger import post_transaction
from services.payments.processor import run_batch
from shared.config import settings


def list_accounts():
    return {"accounts": [], "env": settings.environment}


def transfer_funds(account_id: str, amount: float):
    # Violation: API layer calls ledger directly instead of payments gateway.
    return post_transaction(account_id, amount)


def nightly_batch():
    return run_batch()
