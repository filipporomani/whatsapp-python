import logging
import requests
from typing import Dict, Any
from ..errors import Handle


def create_button(self, button: Dict[Any, Any]) -> Dict[Any, Any]:
    """
    Method to create a button object to be used in the send_message method.

    This is method is designed to only be used internally by the send_button method.

    Args:
            button[dict]: A dictionary containing the button data
    """
    data = {"type": "list", "action": button.get("action")}
    if button.get("header"):
        data["header"] = {"type": "text", "text": button.get("header")}
    if button.get("body"):
        data["body"] = {"text": button.get("body")}
    if button.get("footer"):
        data["footer"] = {"text": button.get("footer")}
    if button.get("type"):
        data["type"] = button.get("type")
    return data


def send_button(
    self, button: Dict[Any, Any], recipient_id: str, sender=None
) -> Dict[Any, Any]:
    """
    Sends an interactive buttons message to a WhatsApp user

    Args:
        button[dict]: A dictionary containing the button data(rows-title may not exceed 20 characters)
        recipient_id[str]: Phone number of the user with country code wihout +

    check https://github.com/Neurotech-HQ/whatsapp#sending-interactive-reply-buttons for an example.
    """
    try:
        sender = dict(self.l)[sender]

    except:
        sender = self.phone_number_id

    if sender == None:
        sender = self.phone_number_id

    url = f"https://graph.facebook.com/{self.LATEST}/{sender}/messages"
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "interactive",
        "interactive": self.create_button(button),
    }
    logging.info(f"Sending buttons to {recipient_id}")
    r = requests.post(url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Buttons sent to {recipient_id}")
        return r.json()
    logging.info(f"Buttons not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return Handle(r.json())


def send_reply_button(
    self, button: Dict[Any, Any], recipient_id: str, sender=None
) -> Dict[Any, Any]:
    """
    Sends an interactive reply buttons[menu] message to a WhatsApp user

    Args:
        button[dict]: A dictionary containing the button data
        recipient_id[str]: Phone number of the user with country code wihout +

    Note:
        The maximum number of buttons is 3, more than 3 buttons will rise an error.
    """
    try:
        sender = dict(self.l)[sender]

    except:
        sender = self.phone_number_id

    if sender == None:
        sender = self.phone_number_id

    url = f"https://graph.facebook.com/{self.LATEST}/{sender}/messages"
    if len(button["action"]["buttons"]) > 3:
        raise ValueError("The maximum number of buttons is 3.")

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": button,
    }
    r = requests.post(url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Reply buttons sent to {recipient_id}")
        return r.json()
    logging.info(f"Reply buttons not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return Handle(r.json())


def send_cta_url(
    self,
    body: str,
    display_text: str,
    url: str,
    recipient_id: str,
    header: str = None,
    footer: str = None,
    sender=None,
) -> Dict[Any, Any]:
    """
    Sends an interactive Call-to-Action URL button message.

    REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/messages/interactive-cta-url-messages
    """
    try:
        sender = dict(self.l)[sender]
    except Exception:
        sender = self.phone_number_id

    if sender is None:
        sender = self.phone_number_id

    endpoint = f"https://graph.facebook.com/{self.LATEST}/{sender}/messages"
    interactive: Dict[Any, Any] = {
        "type": "cta_url",
        "body": {"text": body},
        "action": {
            "name": "cta_url",
            "parameters": {"display_text": display_text, "url": url},
        },
    }
    if header:
        interactive["header"] = {"type": "text", "text": header}
    if footer:
        interactive["footer"] = {"text": footer}

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": interactive,
    }
    logging.info(f"Sending CTA URL to {recipient_id}")
    r = requests.post(endpoint, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"CTA URL sent to {recipient_id}")
        return r.json()
    logging.info(f"CTA URL not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return Handle(r.json())


def send_location_request(
    self, body: str, recipient_id: str, sender=None
) -> Dict[Any, Any]:
    """
    Sends a location request message that prompts the user to share their location.

    REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages/location-request-messages
    """
    try:
        sender = dict(self.l)[sender]
    except Exception:
        sender = self.phone_number_id

    if sender is None:
        sender = self.phone_number_id

    endpoint = f"https://graph.facebook.com/{self.LATEST}/{sender}/messages"
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "interactive",
        "interactive": {
            "type": "location_request_message",
            "body": {"text": body},
            "action": {"name": "send_location"},
        },
    }
    logging.info(f"Sending location request to {recipient_id}")
    r = requests.post(endpoint, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Location request sent to {recipient_id}")
        return r.json()
    logging.info(f"Location request not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return Handle(r.json())
