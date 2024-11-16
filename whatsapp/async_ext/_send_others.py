from typing import Any, Dict, List
import aiohttp
import asyncio
import logging


async def send_custom_json(
    self, data: dict, recipient_id: str = "", sender=None
) -> asyncio.Future:
    """
    Sends a custom json to a WhatsApp user. This can be used to send custom objects to the message endpoint.

    Args:
        data[dict]: Dictionary that should be send
        recipient_id[str]: Phone number of the user with country code wihout +
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_custom_json({
                "messaging_product": "whatsapp",
                "type": "audio",
                "audio": {"id": audio}}, "5511999999999")
    """
    try:
        sender = dict(self.l)[sender]

    except:
        sender = self.phone_number_id

    if sender == None:
        sender = self.phone_number_id

    url = f"https://graph.facebook.com/{self.LATEST}/{sender}/messages"

    if recipient_id:
        if "to" in data.keys():
            data_recipient_id = data["to"]
            logging.info(
                f"Recipient Id is defined in data ({data_recipient_id}) and recipient_id parameter ({recipient_id})"
            )
        else:
            data["to"] = recipient_id

    logging.info(f"Sending custom json to {recipient_id}")

    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Custom json sent to {recipient_id}")
                    return await r.json()
                logging.info(f"Custom json not sent to {recipient_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()

    f = asyncio.ensure_future(call())
    await asyncio.sleep(0.001)  # make asyncio run the task
    return f


async def send_contacts(
    self, contacts: List[Dict[Any, Any]], recipient_id: str, sender=None
) -> asyncio.Future:
    """send_contacts

    Send a list of contacts to a user

    Args:
        contacts(List[Dict[Any, Any]]): List of contacts to send
        recipient_id(str): Phone number of the user with country code wihout +

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> contacts = [{
            "addresses": [{
                "street": "STREET",
                "city": "CITY",
                "state": "STATE",
                "zip": "ZIP",
                "country": "COUNTRY",
                "country_code": "COUNTRY_CODE",
                "type": "HOME"
                },
            ....
            }
        ]

    REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#contacts-object
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
        "type": "contacts",
        "contacts": contacts,
    }
    logging.info(f"Sending contacts to {recipient_id}")

    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Contacts sent to {recipient_id}")
                    return await r.json()
                logging.info(f"Contacts not sent to {recipient_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()

    f = asyncio.ensure_future(call())
    await asyncio.sleep(0.001)  # make asyncio run the task
    return f
