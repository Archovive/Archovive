"""Auth middleware."""

from shared.logging_util import audit_log


def require_token(headers: dict) -> bool:
    audit_log("auth.check", headers.get("Authorization", ""))
    return bool(headers.get("Authorization"))
