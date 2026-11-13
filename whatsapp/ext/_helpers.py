"""Shared helpers for sync Cloud API request builders."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Union


def resolve_sender(client, sender=None) -> str:
    """Resolve a friendly sender key to a WhatsApp phone number ID."""
    try:
        return dict(client.l)[sender]
    except Exception:
        pass
    return client.phone_number_id if sender is None else sender


def messages_url(client, sender=None) -> str:
    phone_id = resolve_sender(client, sender)
    return f"https://graph.facebook.com/{client.LATEST}/{phone_id}/messages"


def text_object(value: Union[str, Mapping[str, Any]], *, field: str = "text") -> Dict[str, Any]:
    """Normalize string or mapping inputs into Cloud API text objects."""
    if isinstance(value, Mapping):
        if "text" in value and "type" not in value and field == "header":
            return {"type": "text", "text": value["text"]}
        if "type" in value:
            return dict(value)
        return dict(value)
    if field == "header":
        return {"type": "text", "text": value}
    return {"text": value}


def optional_header_footer(
    interactive: Dict[str, Any],
    *,
    header: Optional[Union[str, Mapping[str, Any]]] = None,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
) -> Dict[str, Any]:
    if header:
        interactive["header"] = text_object(header, field="header")
    if footer:
        interactive["footer"] = text_object(footer, field="footer")
    return interactive
