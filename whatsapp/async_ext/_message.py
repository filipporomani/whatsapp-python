import logging
import aiohttp
import asyncio


async def react(self, emoji: str) -> asyncio.Future:
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": self.sender,
        "type": "reaction",
        "reaction": {"message_id": self.id, "emoji": emoji},
    }
    logging.info(f"Reacting to {self.id}")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Reacted to {self.id}")
                    return await r.json()
                logging.info(f"Reaction not sent to {self.id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
            
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f


async def send_template(self, template: str, recipient_id: str, components: str = None, lang: str = "en_US", sender = None) -> asyncio.Future:
    """
    Sends a template message to a WhatsApp user, Template messages can either be;
        1. Text template
        2. Media based template
        3. Interactive template
    You can customize the template message by passing a dictionary of components.
    You can find the available components in the documentation.
    https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates
    Args:
        template[str]: Template name to be sent to the user
        recipient_id[str]: Phone number of the user with country code wihout +
        lang[str]: Language of the template message
        components[list]: List of components to be sent to the user  # \
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_template("hello_world", "5511999999999", lang="en_US"))
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
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": lang},
            "components": components,
        },
    }
    logging.info(f"Sending template to {recipient_id}")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Template sent to {recipient_id}")
                    return await r.json()
                logging.info(f"Template not sent to {recipient_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f


# MESSAGE()

async def reply(self, reply_text: str = "", preview_url: bool = True) -> asyncio.Future:
    if self.data == {}:
        return {"error": "No data provided"}
    author = self.instance.get_author(self.data)
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": str(author),
        "type": "text",
        "context": {"message_id": self.id},
        "text": {"preview_url": preview_url, "body": reply_text},
    }
    logging.info(f"Replying to {self.id}")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, json=payload) as r:
                if r.status == 200:
                    logging.info(f"Replied to {self.id}")
                    return await r.json()
                logging.info(f"Reply not sent to {self.id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
            
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f


async def mark_as_read(self) -> asyncio.Future:
    payload = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": self.id,
    }

    logging.info(f"Marking message {self.id} as read")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, json=payload) as r:
                if r.status == 200:
                    logging.info(f"Message {self.id} marked as read")
                    return await r.json()
                logging.info(f"Error marking message {self.id} as read")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
            
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f


async def send(self, preview_url: bool = True) -> asyncio.Future:
    url = f"https://graph.facebook.com/{self.LATEST}/{self.sender}/messages"
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": self.rec,
        "to": self.to,
        "type": "text",
        "text": {"preview_url": preview_url, "body": self.content},
    }
    logging.info(f"Sending message to {self.to}")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=data) as r:
                if r.status == 200:
                    logging.info(f"Message sent to {self.to}")
                    return await r.json()
                logging.info(f"Message not sent to {self.to}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
            
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f
