import logging
import aiohttp
import asyncio
from typing import Dict, Any


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


async def send_button(
    self, button: Dict[Any, Any], recipient_id: str, sender=None
) -> asyncio.Future:
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

    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Buttons sent to {recipient_id}")
                    return await r.json()
                logging.info(f"Buttons not sent to {recipient_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()

    f = asyncio.ensure_future(call())
    await asyncio.sleep(0.001)  # make asyncio run the task
    return f


async def send_reply_button(
    self, button: Dict[Any, Any], recipient_id: str, sender=None
) -> asyncio.Future:
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
    logging.info(f"Sending buttons to {recipient_id}")

    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Buttons sent to {recipient_id}")
                    return await r.json()
                logging.info(f"Buttons not sent to {recipient_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()

    f = asyncio.ensure_future(call())
    await asyncio.sleep(0.001)  # make asyncio run the task
    return f
