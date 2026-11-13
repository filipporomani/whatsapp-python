"""Async interactive Cloud API helpers beyond lists/reply buttons."""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Mapping, Optional, Union

import aiohttp

from ._helpers import messages_url, optional_header_footer, text_object


async def _post_interactive(
    self, recipient_id: str, interactive: Dict[str, Any], sender=None
) -> asyncio.Future:
    endpoint = messages_url(self, sender)
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": interactive,
    }

    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, headers=self.headers, json=data) as r:
                payload = await r.json()
                if r.status == 200:
                    return payload
                logging.error("Request failed (status=%s)", r.status)
                return payload

    f = asyncio.ensure_future(call())
    await asyncio.sleep(0.001)
    return f


async def send_flow(
    self,
    body: str,
    recipient_id: str,
    flow_cta: str,
    *,
    flow_id: Optional[str] = None,
    flow_name: Optional[str] = None,
    flow_token: Optional[str] = None,
    flow_action: str = "navigate",
    flow_action_payload: Optional[Mapping[str, Any]] = None,
    header: Optional[Union[str, Mapping[str, Any]]] = None,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
    flow_message_version: str = "3",
    sender=None,
) -> asyncio.Future:
    """Send a WhatsApp Flows interactive message."""
    if bool(flow_id) == bool(flow_name):
        raise ValueError("Provide exactly one of flow_id or flow_name")

    parameters: Dict[str, Any] = {
        "flow_message_version": flow_message_version,
        "flow_cta": flow_cta,
        "flow_action": flow_action,
    }
    if flow_id:
        parameters["flow_id"] = flow_id
    if flow_name:
        parameters["flow_name"] = flow_name
    if flow_token:
        parameters["flow_token"] = flow_token
    if flow_action_payload:
        parameters["flow_action_payload"] = dict(flow_action_payload)

    interactive: Dict[str, Any] = {
        "type": "flow",
        "body": {"text": body},
        "action": {"name": "flow", "parameters": parameters},
    }
    optional_header_footer(interactive, header=header, footer=footer)
    logging.info("Sending Flow message to %s", recipient_id)
    return await _post_interactive(self, recipient_id, interactive, sender=sender)


async def send_catalog_message(
    self,
    body: str,
    recipient_id: str,
    *,
    thumbnail_product_retailer_id: Optional[str] = None,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
    sender=None,
) -> asyncio.Future:
    action: Dict[str, Any] = {"name": "catalog_message"}
    if thumbnail_product_retailer_id:
        action["parameters"] = {
            "thumbnail_product_retailer_id": thumbnail_product_retailer_id
        }
    interactive: Dict[str, Any] = {
        "type": "catalog_message",
        "body": {"text": body},
        "action": action,
    }
    optional_header_footer(interactive, footer=footer)
    logging.info("Sending catalog message to %s", recipient_id)
    return await _post_interactive(self, recipient_id, interactive, sender=sender)


async def send_product(
    self,
    recipient_id: str,
    catalog_id: str,
    product_retailer_id: str,
    *,
    body: Optional[str] = None,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
    sender=None,
) -> asyncio.Future:
    interactive: Dict[str, Any] = {
        "type": "product",
        "action": {
            "catalog_id": catalog_id,
            "product_retailer_id": product_retailer_id,
        },
    }
    if body:
        interactive["body"] = {"text": body}
    optional_header_footer(interactive, footer=footer)
    logging.info("Sending product message to %s", recipient_id)
    return await _post_interactive(self, recipient_id, interactive, sender=sender)


async def send_product_list(
    self,
    recipient_id: str,
    catalog_id: str,
    header: Union[str, Mapping[str, Any]],
    body: str,
    sections: List[Mapping[str, Any]],
    *,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
    sender=None,
) -> asyncio.Future:
    interactive: Dict[str, Any] = {
        "type": "product_list",
        "header": text_object(header, field="header"),
        "body": {"text": body},
        "action": {"catalog_id": catalog_id, "sections": list(sections)},
    }
    optional_header_footer(interactive, footer=footer)
    logging.info("Sending product list to %s", recipient_id)
    return await _post_interactive(self, recipient_id, interactive, sender=sender)


async def send_address_message(
    self,
    body: str,
    recipient_id: str,
    *,
    country: str,
    header: Optional[Union[str, Mapping[str, Any]]] = None,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
    parameters: Optional[Mapping[str, Any]] = None,
    sender=None,
) -> asyncio.Future:
    params = dict(parameters or {})
    params.setdefault("country", country)
    interactive: Dict[str, Any] = {
        "type": "address_message",
        "body": {"text": body},
        "action": {"name": "address_message", "parameters": params},
    }
    optional_header_footer(interactive, header=header, footer=footer)
    logging.info("Sending address message to %s", recipient_id)
    return await _post_interactive(self, recipient_id, interactive, sender=sender)


async def send_call_permission_request(
    self,
    recipient_id: str,
    *,
    body: Optional[str] = None,
    header: Optional[Union[str, Mapping[str, Any]]] = None,
    footer: Optional[Union[str, Mapping[str, Any]]] = None,
    sender=None,
) -> asyncio.Future:
    interactive: Dict[str, Any] = {
        "type": "call_permission_request",
        "action": {"name": "call_permission_request"},
    }
    if body:
        interactive["body"] = {"text": body}
    optional_header_footer(interactive, header=header, footer=footer)
    logging.info("Sending call permission request to %s", recipient_id)
    return await _post_interactive(self, recipient_id, interactive, sender=sender)
