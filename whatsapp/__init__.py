"""
Unofficial Python wrapper for the WhatsApp Cloud API.
"""
from __future__ import annotations
import requests
import logging
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException, Request
from uvicorn import run as _run
from .constants import VERSION
from .ext._property import authorized
from .ext._send_others import send_custom_json, send_contacts
from .ext._message import send_template
from .ext._send_media import send_image, send_video, send_audio, send_location, send_sticker, send_document
from .ext._media import upload_media, query_media_url, download_media, delete_media
from .ext._buttons import send_button, create_button, send_reply_button
from .ext._static import is_message, get_mobile, get_author, get_name, get_message, get_message_id, get_message_type, get_message_timestamp, get_audio, get_delivery, get_document, get_image, get_sticker, get_interactive_response, get_location, get_video, changed_field
import json


class WhatsApp(object):
    def __init__(self, token: str = "", phone_number_id: dict = "", logger: bool = True, update_check: bool = True, verify_token: str = "", debug: bool = True, version: str = "latest"):
        """
        Initialize the WhatsApp Object

        Args:
            token[str]: Token for the WhatsApp cloud API obtained from the Facebook developer portal
            phone_number_id[str]: Phone number id for the WhatsApp cloud API obtained from the developer portal
            logger[bool]: Whether to enable logging or not (default: True)
        """

        # Check if the version is up to date
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        self.l = phone_number_id

        if isinstance(phone_number_id, dict):
            # use first phone number id as default
            phone_number_id = phone_number_id[list(phone_number_id.keys())[0]]

        elif phone_number_id == "":
            logging.error("Phone number ID not provided")
            raise ValueError(
                "Phone number ID not provided but required")
        elif isinstance(phone_number_id, str):
            logging.critical(
                "The phone number ID should be a dictionary of phone numbers and their IDs. Using strings is deprecated.")
            raise ValueError(
                "Phone number ID should be a dictionary of phone numbers and their IDs")
        else:
            pass

        self.VERSION = VERSION  # package version
        r = requests.get("https://developers.facebook.com/docs/graph-api/changelog/").text

        # dynamically get the latest version of the API
        if version == "latest":
            soup = BeautifulSoup(r, features="html.parser")
            t1 = soup.findAll("table")

            def makeversion(table):
                result = []
                allrows = table.findAll('tr')
                for row in allrows:
                    result.append([])
                    allcols = row.findAll('td')
                    for col in allcols:
                        thestrings = [(s) for s in col.findAll(text=True)]
                        thetext = ''.join(thestrings)
                        result[-1].append(thetext)
                return result[0][1]
            self.LATEST = makeversion(t1[0])  # latest version of the API
        else:
            self.LATEST = version

        if update_check is True:
            latest = str(requests.get(
                "https://pypi.org/pypi/whatsapp-python/json").json()["info"]["version"])
            if self.VERSION != latest:
                try:
                    version_int = int(self.VERSION.replace(".", ""))
                except:
                    version_int = 0
                try:
                    latest_int = int(latest.replace(".", ""))
                except:
                    latest_int = 0
                # this is to avoid the case where the version is 1.0.10 and the latest is 1.0.2 (possible if user is using the github version)
                if version_int < latest_int:
                    if version_int == 0:
                        logging.critical(
                            f"There was an error while checking for updates, please check for updates manually. This may be due to the version being a post-release version (e.g. 1.0.0.post1) or a pre-release version (e.g. 1.0.0a1). READ THE CHANGELOG BEFORE UPDATING. NEW VERSIONS MAY BREAK YOUR CODE IF NOT PROPERLY UPDATED.")
                    else:
                        logging.critical(
                            f"Whatsapp-python is out of date. Please update to the latest version {latest}. READ THE CHANGELOG BEFORE UPDATING. NEW VERSIONS MAY BREAK YOUR CODE IF NOT PROPERLY UPDATED.")

        if token == "":
            logging.error("Token not provided")
            raise ValueError("Token not provided but required")
        if phone_number_id == "":
            logging.error("Phone number ID not provided")
            raise ValueError(
                "Phone number ID not provided but required")
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = f"https://graph.facebook.com/{self.LATEST}"
        self.url = f"{self.base_url}/{phone_number_id}/messages"
        self.verify_token = verify_token

        async def base(*args):
            pass
        self.message_handler = base
        self.other_handler = base
        self.verification_handler = base
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        if logger is False:
            logging.disable(logging.INFO)
            logging.disable(logging.ERROR)
        if debug is False:
            logging.disable(logging.DEBUG)
            logging.disable(logging.ERROR)

        self.app = FastAPI()

        # Verification handler has 1 argument: challenge (str | bool): str if verification is successful, False if not

        @self.app.get("/")
        async def verify_endpoint(r: Request):
            if r.query_params.get("hub.verify_token") == self.verify_token:
                logging.debug("Webhook verified successfully")
                challenge = r.query_params.get("hub.challenge")
                self.verification_handler(challenge)
                self.other_handler(challenge)
                return int(challenge)
            logging.error("Webhook Verification failed - token mismatch")
            await self.verification_handler(False)
            await self.other_handler(False)
            return {"success": False}

        @self.app.post("/")
        async def hook(r: Request):
            try:
                # Handle Webhook Subscriptions
                data = await r.json()
                if data is None:
                    return {"success": False}
                data_str = json.dumps(data, indent=4)
                # log the data received only if the log level is debug
                logging.debug(f"Received webhook data: {data_str}")

                changed_field = self.changed_field(data)
                if changed_field == "messages":
                    new_message = self.is_message(data)
                    if new_message:
                        msg = Message(instance=self, data=data)
                        await self.message_handler(msg)
                        await self.other_handler(msg)
                return {"success": True}
            except Exception as e:
                logging.error(f"Error parsing message: {e}")
                raise HTTPException(status_code=500, detail={
                    "success": False,
                    "error": str(e)
                })

    # all the files starting with _ are imported here, and should not be imported directly.

    is_message = staticmethod(is_message)
    get_mobile = staticmethod(get_mobile)
    get_name = staticmethod(get_name)
    get_message = staticmethod(get_message)
    get_message_id = staticmethod(get_message_id)
    get_message_type = staticmethod(get_message_type)
    get_message_timestamp = staticmethod(get_message_timestamp)
    get_audio = staticmethod(get_audio)
    get_delivery = staticmethod(get_delivery)
    get_document = staticmethod(get_document)
    get_image = staticmethod(get_image)
    get_sticker = staticmethod(get_sticker)
    get_interactive_response = staticmethod(get_interactive_response)
    get_location = staticmethod(get_location)
    get_video = staticmethod(get_video)
    changed_field = staticmethod(changed_field)
    get_author = staticmethod(get_author)

    send_button = send_button
    create_button = create_button
    send_reply_button = send_reply_button
    send_image = send_image
    send_video = send_video
    send_audio = send_audio
    send_location = send_location
    send_sticker = send_sticker
    send_document = send_document
    upload_media = upload_media
    query_media_url = query_media_url
    download_media = download_media
    delete_media = delete_media
    send_template = send_template
    send_custom_json = send_custom_json
    send_contacts = send_contacts

    authorized = property(authorized)

    def create_message(self, **kwargs) -> Message:
        """
        Create a message object

        Args:
            data[dict]: The message data
            content[str]: The message content
            to[str]: The recipient
            rec_type[str]: The recipient type (individual/group)
        """
        return Message(**kwargs, instance=self)

    def on_message(self, handler: function):
        """
        Set the handler for incoming messages

        Args:
            handler[function]: The handler function
        """
        self.message_handler = handler

    def on_event(self, handler: function):
        """
        Set the handler for other events

        Args:
            handler[function]: The handler function
        """
        self.other_handler = handler

    def on_verification(self, handler: function):
        """
        Set the handler for verification

        Args:
            handler[function]: The handler function
        """
        self.verification_handler = handler

    def run(self, host: str = "localhost", port: int = 5000, **options):
        _run(self.app, host=host, port=port, **options)


class Message(object):
    # type: ignore
    def __init__(self, id: int = None, data: dict = {}, instance: WhatsApp = None, content: str = "", to: str = "", rec_type: str = "individual"):
        self.instance = instance
        self.url = self.instance.url
        self.headers = self.instance.headers

        try:
            self.id = instance.get_message_id(data)
        except:
            self.id = id
        try:
            self.type = self.instance.get_message_type(data)
        except:
            self.type = "text"
        self.data = data
        self.rec = rec_type
        self.to = to
        try:
            self.content = content if content != "" else self.instance.get_message(
                data)
        except:
            self.content = content
        try:
            self.name = self.instance.get_name(data)
        except:
            self.name = None

        if self.type == "image":
            try:
                self.image = self.instance.get_image(data)
            except:
                self.image = None
        if self.type == "sticker":
            try:
                self.sticker = self.instance.get_sticker(data)
            except:
                self.sticker = None
        elif self.type == "video":
            try:
                self.video = self.instance.get_video(data)
            except:
                self.video = None
        elif self.type == "audio":
            try:
                self.audio = self.instance.get_audio(data)
            except:
                pass
        elif self.type == "document":
            try:
                self.document = self.instance.get_document(data)
            except:
                pass
        elif self.type == "location":
            try:
                self.location = self.instance.get_location(data)
            except:
                pass
        elif self.type == "interactive":
            try:
                self.interactive = self.instance.get_interactive_response(data)
            except:
                pass

    def reply(self, reply_text: str = "", preview_url: bool = True) -> dict:
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
        r = requests.post(self.url, headers=self.headers, json=payload)
        if r.status_code == 200:
            logging.info(f"Message sent to {self.instance.get_author(self.data)}")
            return r.json()
        logging.info(f"Message not sent to {self.instance.get_author(self.data)}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def mark_as_read(self) -> dict:

        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": self.id,
        }

        response = requests.post(
            f"{self.instance.url}", headers=self.instance.headers, json=payload)
        if response.status_code == 200:
            logging.info(response.json())
            return response.json()
        else:
            logging.error(response.json())
            return response.json()

    def send(self, sender=None, preview_url: bool = True) -> dict:

        try:
            sender = dict(self.instance.l)[sender]

        except:
            sender = self.instance.phone_number_id

        if sender == None:
            sender = self.instance.phone_number_id

        url = f"https://graph.facebook.com/{self.instance.LATEST}/{sender}/messages"
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": self.rec,
            "to": self.to,
            "type": "text",
            "text": {"preview_url": preview_url, "body": self.content},
        }
        logging.info(f"Sending message to {self.to}")
        r = requests.post(url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Message sent to {self.to}")
            return r.json()
        logging.info(f"Message not sent to {self.to}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def react(self, emoji: str) -> dict:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "reaction",
            "reaction": {"message_id": self.id, "emoji": emoji},
        }
        logging.info(f"Reacting to {self.id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Reaction sent to {self.to}")
            return r.json()
        logging.info(f"Reaction not sent to {self.to}")
        logging.info(f"Status code: {r.status_code}")
        logging.debug(f"Response: {r.json()}")
        return r.json()
