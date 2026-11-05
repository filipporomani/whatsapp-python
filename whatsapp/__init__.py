"""
Unofficial Python wrapper for the WhatsApp Cloud API.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Optional, Union

import aiohttp
import requests
from fastapi import FastAPI, HTTPException, Request
from uvicorn import run as _run

from .constants import VERSION
from .errors import Handle
from .graph_api import resolve_graph_api_version
from .ext._property import authorized
from .ext._send_others import send_custom_json, send_contacts
from .ext._message import send_template
from .ext._send_media import (
    send_image,
    send_video,
    send_audio,
    send_location,
    send_sticker,
    send_document,
)
from .ext._media import upload_media, query_media_url, download_media, delete_media
from .ext._buttons import (
    send_button,
    create_button,
    send_reply_button,
    send_cta_url,
    send_location_request,
)
from .ext._static import (
    is_message,
    get_mobile,
    get_author,
    get_name,
    get_message,
    get_message_id,
    get_message_type,
    get_message_timestamp,
    get_audio,
    get_delivery,
    get_document,
    get_image,
    get_sticker,
    get_interactive_response,
    get_location,
    get_video,
    get_reaction,
    changed_field,
)

from .async_ext._property import authorized as async_authorized
from .async_ext._send_others import (
    send_custom_json as async_send_custom_json,
    send_contacts as async_send_contacts,
)
from .async_ext._message import send_template as async_send_template
from .async_ext._send_media import (
    send_image as async_send_image,
    send_video as async_send_video,
    send_audio as async_send_audio,
    send_location as async_send_location,
    send_sticker as async_send_sticker,
    send_document as async_send_document,
)
from .async_ext._media import (
    upload_media as async_upload_media,
    query_media_url as async_query_media_url,
    download_media as async_download_media,
    delete_media as async_delete_media,
)
from .async_ext._buttons import (
    send_button as async_send_button,
    create_button as async_create_button,
    send_reply_button as async_send_reply_button,
    send_cta_url as async_send_cta_url,
    send_location_request as async_send_location_request,
)
from .async_ext._static import (
    is_message as async_is_message,
    get_mobile as async_get_mobile,
    get_author as async_get_author,
    get_name as async_get_name,
    get_message as async_get_message,
    get_message_id as async_get_message_id,
    get_message_type as async_get_message_type,
    get_message_timestamp as async_get_message_timestamp,
    get_audio as async_get_audio,
    get_delivery as async_get_delivery,
    get_document as async_get_document,
    get_image as async_get_image,
    get_sticker as async_get_sticker,
    get_interactive_response as async_get_interactive_response,
    get_location as async_get_location,
    get_video as async_get_video,
    get_reaction as async_get_reaction,
    changed_field as async_changed_field,
)


def _check_package_update(current_version: str) -> None:
    try:
        latest = str(
            requests.get(
                "https://pypi.org/pypi/whatsapp-python/json", timeout=10
            ).json()["info"]["version"]
        )
    except Exception as exc:  # noqa: BLE001
        logging.debug("Skipped package update check: %s", exc)
        return

    if current_version == latest:
        return

    try:
        version_int = int(current_version.replace(".", ""))
    except ValueError:
        version_int = 0
    try:
        latest_int = int(latest.replace(".", ""))
    except ValueError:
        latest_int = 0

    # Avoid false positives such as 1.0.10 vs 1.0.2 when using local builds.
    if version_int >= latest_int:
        return

    if version_int == 0:
        logging.critical(
            "There was an error while checking for updates, please check for "
            "updates manually. This may be due to the version being a "
            "post-release version (e.g. 1.0.0.post1) or a pre-release version "
            "(e.g. 1.0.0a1). READ THE CHANGELOG BEFORE UPDATING. NEW VERSIONS "
            "MAY BREAK YOUR CODE IF NOT PROPERLY UPDATED."
        )
    else:
        logging.critical(
            "Whatsapp-python is out of date. Please update to the latest "
            "version %s. READ THE CHANGELOG BEFORE UPDATING. NEW VERSIONS MAY "
            "BREAK YOUR CODE IF NOT PROPERLY UPDATED.",
            latest,
        )


class WhatsApp:
    def __init__(
        self,
        token: str = "",
        phone_number_id: Union[dict, str] = "",
        logger: bool = True,
        update_check: bool = True,
        verify_token: str = "",
        debug: bool = True,
        version: str = "latest",
    ):
        """
        Initialize the WhatsApp Object

        Args:
            token[str]: Token for the WhatsApp cloud API obtained from the Facebook developer portal
            phone_number_id[dict]: Mapping of friendly keys to phone number IDs from the developer portal
            logger[bool]: Whether to enable logging or not (default: True)
            update_check[bool]: Whether to check PyPI for package updates
            verify_token[str]: Verification token used by the webhook challenge
            debug[bool]: Whether to keep debug logs enabled
            version[str]: Graph API version (``\"latest\"`` or e.g. ``\"v27.0\"``)
        """

        logging.getLogger(__name__).addHandler(logging.NullHandler())

        self.l = phone_number_id

        if isinstance(phone_number_id, dict):
            # use first phone number id as default
            phone_number_id = phone_number_id[list(phone_number_id.keys())[0]]
        elif phone_number_id == "":
            logging.error("Phone number ID not provided")
            raise ValueError("Phone number ID not provided but required")
        elif isinstance(phone_number_id, str):
            logging.critical(
                "The phone number ID should be a dictionary of phone numbers and their IDs. Using strings is deprecated."
            )
            raise ValueError(
                "Phone number ID should be a dictionary of phone numbers and their IDs"
            )

        self.VERSION = VERSION
        self.LATEST = resolve_graph_api_version(version)

        if update_check is True:
            _check_package_update(self.VERSION)

        if token == "":
            logging.error("Token not provided")
            raise ValueError("Token not provided but required")
        if phone_number_id == "":
            logging.error("Phone number ID not provided")
            raise ValueError("Phone number ID not provided but required")

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
            "Authorization": f"Bearer {self.token}",
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
                await self.verification_handler(challenge)
                await self.other_handler(challenge)
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
                # Avoid logging raw webhook payloads — they contain phone numbers
                # and message content that CodeQL treats as sensitive clear-text data.
                logging.debug("Received webhook payload")

                changed = self.changed_field(data)
                if changed == "messages":
                    new_message = self.is_message(data)
                    if new_message:
                        msg = self.create_message(data=data)
                        await self.message_handler(msg)
                        await self.other_handler(msg)
                return {"success": True}
            except Exception as e:
                logging.error(f"Error parsing message: {e}")
                raise HTTPException(
                    status_code=500, detail={"success": False, "error": str(e)}
                )

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
    get_reaction = staticmethod(get_reaction)
    changed_field = staticmethod(changed_field)
    get_author = staticmethod(get_author)

    send_button = send_button
    create_button = create_button
    send_reply_button = send_reply_button
    send_cta_url = send_cta_url
    send_location_request = send_location_request
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

    def create_message(self, **kwargs) -> "Message":
        """
        Create a message object

        Args:
            data[dict]: The message data
            content[str]: The message content
            to[str]: The recipient
            rec_type[str]: The recipient type (individual/group)
        """
        return Message(**kwargs, instance=self)

    def on_message(self, handler: Callable[..., Any]):
        """
        Set the handler for incoming messages

        Args:
            handler[function]: The handler function
        """
        self.message_handler = handler

    def on_event(self, handler: Callable[..., Any]):
        """
        Set the handler for other events

        Args:
            handler[function]: The handler function
        """
        self.other_handler = handler

    def on_verification(self, handler: Callable[..., Any]):
        """
        Set the handler for verification

        Args:
            handler[function]: The handler function
        """
        self.verification_handler = handler

    def run(self, host: str = "localhost", port: int = 5000, **options):
        _run(self.app, host=host, port=port, **options)


class AsyncWhatsApp(WhatsApp):
    """Async variant of :class:`WhatsApp` that returns awaitable HTTP calls."""

    is_message = staticmethod(async_is_message)
    get_mobile = staticmethod(async_get_mobile)
    get_name = staticmethod(async_get_name)
    get_message = staticmethod(async_get_message)
    get_message_id = staticmethod(async_get_message_id)
    get_message_type = staticmethod(async_get_message_type)
    get_message_timestamp = staticmethod(async_get_message_timestamp)
    get_audio = staticmethod(async_get_audio)
    get_delivery = staticmethod(async_get_delivery)
    get_document = staticmethod(async_get_document)
    get_image = staticmethod(async_get_image)
    get_sticker = staticmethod(async_get_sticker)
    get_interactive_response = staticmethod(async_get_interactive_response)
    get_location = staticmethod(async_get_location)
    get_video = staticmethod(async_get_video)
    get_reaction = staticmethod(async_get_reaction)
    changed_field = staticmethod(async_changed_field)
    get_author = staticmethod(async_get_author)

    send_button = async_send_button
    create_button = async_create_button
    send_reply_button = async_send_reply_button
    send_cta_url = async_send_cta_url
    send_location_request = async_send_location_request
    send_image = async_send_image
    send_video = async_send_video
    send_audio = async_send_audio
    send_location = async_send_location
    send_sticker = async_send_sticker
    send_document = async_send_document
    upload_media = async_upload_media
    query_media_url = async_query_media_url
    download_media = async_download_media
    delete_media = async_delete_media
    send_template = async_send_template
    send_custom_json = async_send_custom_json
    send_contacts = async_send_contacts
    authorized = property(async_authorized)

    def handle(self, data: dict):
        return Handle(data)

    def create_message(self, **kwargs) -> "AsyncMessage":
        """
        Create an async message object

        Args:
            data[dict]: The message data
            content[str]: The message content
            to[str]: The recipient
            rec_type[str]: The recipient type (individual/group)
        """
        return AsyncMessage(**kwargs, instance=self)


class Message:
    # type: ignore
    def __init__(
        self,
        id: Optional[str] = None,
        data: Optional[dict] = None,
        instance: Optional[WhatsApp] = None,
        content: str = "",
        to: str = "",
        rec_type: str = "individual",
    ):
        data = data or {}
        self.instance = instance
        self.url = self.instance.url
        self.headers = self.instance.headers

        try:
            self.id = instance.get_message_id(data)
        except Exception:
            self.id = id
        try:
            self.type = self.instance.get_message_type(data)
        except Exception:
            self.type = "text"
        self.data = data
        self.rec = rec_type

        try:
            self.to = to if to != "" else self.instance.get_mobile(data)
        except Exception:
            self.to = to

        try:
            self.sender = self.instance.get_author(data) or self.to
        except Exception:
            self.sender = self.to

        try:
            self.content = content if content != "" else self.instance.get_message(data)
        except Exception:
            self.content = content
        try:
            self.name = self.instance.get_name(data)
        except Exception:
            self.name = None

        if self.type == "image":
            try:
                self.image = self.instance.get_image(data)
            except Exception:
                self.image = None
        if self.type == "sticker":
            try:
                self.sticker = self.instance.get_sticker(data)
            except Exception:
                self.sticker = None
        elif self.type == "video":
            try:
                self.video = self.instance.get_video(data)
            except Exception:
                self.video = None
        elif self.type == "audio":
            try:
                self.audio = self.instance.get_audio(data)
            except Exception:
                pass
        elif self.type == "document":
            try:
                self.document = self.instance.get_document(data)
            except Exception:
                pass
        elif self.type == "location":
            try:
                self.location = self.instance.get_location(data)
            except Exception:
                pass
        elif self.type == "interactive":
            try:
                self.interactive = self.instance.get_interactive_response(data)
            except Exception:
                pass
        elif self.type == "reaction":
            try:
                self.reaction = self.instance.get_reaction(data)
            except Exception:
                self.reaction = None

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
        logging.error("Request failed (status=%s)", r.status_code)
        return r.json()

    def mark_as_read(self, typing: bool = False) -> dict:
        """
        Mark this inbound message as read.

        Args:
            typing: When True, also display a typing indicator (dismissed after
                a reply or ~25 seconds). See Meta typing-indicators docs.
        """
        payload: dict[str, Any] = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": self.id,
        }
        if typing:
            payload["typing_indicator"] = {"type": "text"}

        response = requests.post(
            f"{self.instance.url}", headers=self.instance.headers, json=payload
        )
        if response.status_code == 200:
            logging.info("Request succeeded (status=%s)", response.status_code)
            return response.json()
        logging.error("Request failed (status=%s)", response.status_code)
        return response.json()

    def show_typing(self) -> dict:
        """Mark as read and show a typing indicator while preparing a reply."""
        return self.mark_as_read(typing=True)

    def send(self, sender=None, preview_url: bool = True) -> dict:

        try:
            sender = dict(self.instance.l)[sender]

        except Exception:
            sender = self.instance.phone_number_id

        if sender is None:
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
        logging.error("Request failed (status=%s)", r.status_code)
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
        logging.debug("Request failed (status=%s)", r.status_code)
        return r.json()


class AsyncMessage:
    # type: ignore
    def __init__(
        self,
        id: Optional[str] = None,
        data: Optional[dict] = None,
        instance: Optional[WhatsApp] = None,
        content: str = "",
        to: str = "",
        rec_type: str = "individual",
    ):
        data = data or {}
        self.instance = instance
        self.url = self.instance.url
        self.headers = self.instance.headers

        try:
            self.id = instance.get_message_id(data)
        except Exception:
            self.id = id
        try:
            self.type = self.instance.get_message_type(data)
        except Exception:
            self.type = "text"
        self.data = data
        self.rec = rec_type
        try:
            self.to = to if to != "" else self.instance.get_mobile(data)
        except Exception:
            self.to = to
        try:
            self.sender = self.instance.get_author(data) or self.to
        except Exception:
            self.sender = self.to
        try:
            self.content = content if content != "" else self.instance.get_message(data)
        except Exception:
            self.content = content
        try:
            self.name = self.instance.get_name(data)
        except Exception:
            self.name = None

        if self.type == "image":
            try:
                self.image = self.instance.get_image(data)
            except Exception:
                self.image = None
        if self.type == "sticker":
            try:
                self.sticker = self.instance.get_sticker(data)
            except Exception:
                self.sticker = None
        elif self.type == "video":
            try:
                self.video = self.instance.get_video(data)
            except Exception:
                self.video = None
        elif self.type == "audio":
            try:
                self.audio = self.instance.get_audio(data)
            except Exception:
                pass
        elif self.type == "document":
            try:
                self.document = self.instance.get_document(data)
            except Exception:
                pass
        elif self.type == "location":
            try:
                self.location = self.instance.get_location(data)
            except Exception:
                pass
        elif self.type == "interactive":
            try:
                self.interactive = self.instance.get_interactive_response(data)
            except Exception:
                pass
        elif self.type == "reaction":
            try:
                self.reaction = self.instance.get_reaction(data)
            except Exception:
                self.reaction = None

    async def reply(
        self, reply_text: str = "", preview_url: bool = True
    ) -> asyncio.Future:
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
                async with session.post(
                    self.url, headers=self.headers, json=payload
                ) as response:
                    if response.status == 200:
                        logging.info(
                            f"Message sent to {self.instance.get_author(self.data)}"
                        )
                        return await response.json()
                    logging.info(
                        f"Message not sent to {self.instance.get_author(self.data)}"
                    )
                    logging.info(f"Status code: {response.status}")
                    logging.error("Request failed (status=%s)", response.status)
                    return await response.json()

        f = asyncio.ensure_future(call())
        await asyncio.sleep(0.001)  # make asyncio run the task
        return f

    async def mark_as_read(self, typing: bool = False) -> asyncio.Future:
        """
        Mark this inbound message as read.

        Args:
            typing: When True, also display a typing indicator (dismissed after
                a reply or ~25 seconds). See Meta typing-indicators docs.
        """
        payload: dict[str, Any] = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": self.id,
        }
        if typing:
            payload["typing_indicator"] = {"type": "text"}

        async def call():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.instance.url}", headers=self.instance.headers, json=payload
                ) as response:
                    if response.status == 200:
                        logging.info("Request succeeded (status=%s)", response.status)
                        return await response.json()
                    logging.error("Request failed (status=%s)", response.status)
                    return await response.json()

        f = asyncio.ensure_future(call())
        await asyncio.sleep(0.001)  # make asyncio run the task
        return f

    async def show_typing(self) -> asyncio.Future:
        """Mark as read and show a typing indicator while preparing a reply."""
        return await self.mark_as_read(typing=True)

    async def send(self, sender=None, preview_url: bool = True) -> asyncio.Future:
        try:
            sender = dict(self.instance.l)[sender]

        except Exception:
            sender = self.instance.phone_number_id

        if sender is None:
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

        async def call():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, headers=self.headers, json=data
                ) as response:
                    if response.status == 200:
                        logging.info(f"Message sent to {self.to}")
                        return await response.json()
                    logging.info(f"Message not sent to {self.to}")
                    logging.info(f"Status code: {response.status}")
                    logging.error("Request failed (status=%s)", response.status)
                    return await response.json()

        f = asyncio.ensure_future(call())
        await asyncio.sleep(0.001)  # make asyncio run the task
        return f

    async def react(self, emoji: str) -> asyncio.Future:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
            "type": "reaction",
            "reaction": {"message_id": self.id, "emoji": emoji},
        }
        logging.info(f"Reacting to {self.id}")

        async def call():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url, headers=self.headers, json=data
                ) as response:
                    if response.status == 200:
                        logging.info(f"Reaction sent to {self.to}")
                        return await response.json()
                    logging.info(f"Reaction not sent to {self.to}")
                    logging.info(f"Status code: {response.status}")
                    logging.debug("Request failed (status=%s)", response.status)
                    return await response.json()

        f = asyncio.ensure_future(call())
        await asyncio.sleep(0.001)
        return f
