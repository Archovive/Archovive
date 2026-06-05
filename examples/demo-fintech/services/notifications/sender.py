"""Ops notifications."""

from shared.logging_util import audit_log


def notify_ops(message: str) -> None:
    audit_log("notify.ops", message)
