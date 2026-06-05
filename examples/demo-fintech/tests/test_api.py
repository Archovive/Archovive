"""Smoke tests for demo fintech."""

from services.api.routes import list_accounts


def test_list_accounts():
    assert "accounts" in list_accounts()
