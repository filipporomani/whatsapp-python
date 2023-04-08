"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""
from __future__ import annotations

import requests
import logging

# Setup logging
logging.getLogger(__name__).addHandler(logging.NullHandler())


class WhatsApp(object):
    """ "
    WhatsApp Object
    """

    def __init__(self, token: str = "", phone_number_id: str = "", logger: bool = True):
        """
        Initialize the WhatsApp Object

        Args:
            token[str]: Token for the WhatsApp cloud API obtained from the developer portal
            phone_number_id[str]: Phone number id for the WhatsApp cloud API obtained from the developer portal
            logger[bool]: Whether to enable logging or not (default: True)
        """

        # Check if the version is up to date
        self.VERSION = "1.1.2"
        latest = str(requests.get(
            "https://pypi.org/pypi/whatsapp-python/json").json()["info"]["version"])
        if self.VERSION != latest:
            version_int = int(self.VERSION.replace(".", ""))
            latest_int = int(latest.replace(".", ""))
            # this is to avoid the case where the version is 1.0.10 and the latest is 1.0.2 (possible if user is using the github version)
            if version_int < latest_int:
                logging.critical(
                    f"Whatsapp-python is out of date. Please update to the latest version {latest}")

        if token == "" or phone_number_id == "":
            logging.error("Token or phone number id not provided")
            raise ValueError(
                "Token or phone number ID not provided but is required")
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v15.0"
        self.url = f"{self.base_url}/{phone_number_id}/messages"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        if logger is False:
            logging.disable(logging.INFO)
            logging.disable(logging.ERROR)

    @property
    def authorized(self) -> bool:
        return requests.get(self.url, headers=self.headers).status_code != 401
    
    # all the files starting with _ are imported here, and should not be imported directly.

    from ._send_others import send_custom_json, send_contacts
    from ._message import send_message, send_template, reply_to_message, mark_as_read
    from ._send_media import send_image, send_video, send_audio, send_location, send_sticker, send_document
    from ._media import upload_media, query_media_url, download_media, delete_media
    from ._buttons import send_button, create_button, send_reply_button
    from ._static import is_message, get_mobile, get_name, get_message, get_message_id, get_message_type, get_message_timestamp, get_audio, get_delivery, get_document, get_image, get_interactive_response, get_location, get_video, changed_field
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
