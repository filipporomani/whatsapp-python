"""
Unofficial Python wrapper for the WhatsApp Cloud API.
"""
from __future__ import annotations

import requests
import logging
from .constants import VERSION
from .ext._property import authorized
from .ext._send_others import send_custom_json, send_contacts
from .ext._message import send_template
from .ext._send_media import send_image, send_video, send_audio, send_location, send_sticker, send_document
from .ext._media import upload_media, query_media_url, download_media, delete_media
from .ext._buttons import send_button, create_button, send_reply_button
from .ext._static import is_message, get_mobile, get_author, get_name, get_message, get_message_id, get_message_type, get_message_timestamp, get_audio, get_delivery, get_document, get_image, get_interactive_response, get_location, get_video, changed_field
import json


class WhatsApp(object):
    def __init__(self, token: str = "", phone_number_id: str = "", logger: bool = True, update_check: bool = True, verify_token: str = "", debug: bool = True):
        """
        Initialize the WhatsApp Object

        Args:
            token[str]: Token for the WhatsApp cloud API obtained from the Facebook developer portal
            phone_number_id[str]: Phone number id for the WhatsApp cloud API obtained from the developer portal
            logger[bool]: Whether to enable logging or not (default: True)
        """

        # Check if the version is up to date
        logging.getLogger(__name__).addHandler(logging.NullHandler())

        self.VERSION = VERSION
        # if update_check is True:
        #     latest = str(requests.get(
        #         "https://pypi.org/pypi/whatsapp-python/json").json()["info"]["version"])
        #     if self.VERSION != latest:
        #         try:
        #             version_int = int(self.VERSION.replace(".", ""))
        #         except:
        #             version_int = 0
        #         latest_int = int(latest.replace(".", ""))
        #         # this is to avoid the case where the version is 1.0.10 and the latest is 1.0.2 (possible if user is using the github version)
        #         if version_int < latest_int:
        #             if version_int == 0:
        #                 logging.critical(
        #                     f"There was an error while checking for updates, please update the package manually or report the issue on GitHub.")
        #             else:
        #                 logging.critical(
        #                     f"Whatsapp-python is out of date. Please update to the latest version {latest}. READ THE CHANGELOG BEFORE UPDATING. NEW VERSIONS MAY BREAK YOUR CODE IF NOT PROPERLY UPDATED.")

        if token == "":
            logging.error("Token not provided")
            raise ValueError("Token not provided but required")
        if phone_number_id == "":
            logging.error("Phone number ID not provided")
            raise ValueError(
                "Phone number ID not provided but required")
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v18.0"
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

        # Verification handler has 1 argument: challenge (str | bool): str if verification is successful, False if not

    async def verify_endpoint(self, query_params: dict):
        if query_params.get("hub.verify_token") == self.verify_token:
            logging.debug("Webhook verified successfully")
            challenge = query_params.get("hub.challenge")
            self.verification_handler(challenge)
            self.other_handler(challenge)
            return int(challenge)
        logging.error("Webhook Verification failed - token mismatch")
        await self.verification_handler(False)
        await self.other_handler(False)
        return {"success": False}

    async def hook(request: dict):
        try:
            # Handle Webhook Subscriptions
            data = request.get('data')
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


class Message(object):
    def __init__(self, id: int = None, data: dict = {}, instance: WhatsApp = None, content: str = "", to: str = "", rec_type: str = "individual"):  # type: ignore
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
            self.sender = self.instance.get_mobile(data)
        except:
            self.sender = None
        try:
            self.name = self.instance.get_name(data)
        except:
            self.name = None

        if self.type == "image":
            try:
                self.image = self.instance.get_image(data)
            except:
                self.image = None
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

    from .ext._message import send, reply, mark_as_read
