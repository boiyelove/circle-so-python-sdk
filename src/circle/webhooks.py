"""Webhook signature verification and payload parsing."""
from __future__ import annotations
import hashlib
import hmac
from typing import Any, Dict, Optional
from circle.models.base import CircleModel


class WebhookEvent(CircleModel):
    event_type: Optional[str] = None
    community_id: Optional[int] = None
    data: Optional[Dict[str, Any]] = None


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify HMAC-SHA256 webhook signature.

    Args:
        payload: Raw request body bytes.
        signature: Signature from the webhook header.
        secret: Your webhook signing secret.

    Returns:
        True if signature is valid.
    """
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def parse_webhook(payload: Dict[str, Any]) -> WebhookEvent:
    """Parse a webhook payload into a typed WebhookEvent.

    Args:
        payload: Parsed JSON body from the webhook request.

    Returns:
        WebhookEvent with event_type, community_id, and data.
    """
    return WebhookEvent.model_validate(payload)
