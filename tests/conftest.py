"""Shared fixtures for kernel contract tests."""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def demo_job(repo_root: Path) -> dict:
    from tests._contract_helpers import canonical_demo_job

    return canonical_demo_job(repo_root)
