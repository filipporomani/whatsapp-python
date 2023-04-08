import logging
import requests
from typing import Dict, Any


def send_message(
    self, message: str, recipient_id: str, recipient_type: str = "individual", preview_url: bool = True
):
    """
     Sends a text message to a WhatsApp user

     Args:
            message[str]: Message to be sent to the user
            recipient_id[str]: Phone number of the user with country code wihout +
            recipient_type[str]: Type of the recipient, either individual or group
            preview_url[bool]: Whether to send a preview url or not

    Example:
        ```python
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_message("Hello World", "5511999999999")
        >>> whatsapp.send_message("Hello World", "5511999999999", preview_url=False)

    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": recipient_type,
        "to": recipient_id,
        "type": "text",
        "text": {"preview_url": preview_url, "body": message},
    }
    logging.info(f"Sending message to {recipient_id}")
    r = requests.post(f"{self.url}", headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Message sent to {recipient_id}")
        return r.json()
    logging.info(f"Message not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()


def reply_to_message(
    self, message_id: str, recipient_id: str, message: str, preview_url: bool = True
):
    """
    Replies to a message

    Args:
        message_id[str]: Message id of the message to be replied to
        recipient_id[str]: Phone number of the user with country code wihout +
        message[str]: Message to be sent to the user
        preview_url[bool]: Whether to send a preview url or not
    """
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient_id,
        "type": "text",
        "context": {"message_id": message_id},
        "text": {"preview_url": preview_url, "body": message},
    }

    logging.info(f"Replying to {message_id}")
    r = requests.post(f"{self.url}", headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Message sent to {recipient_id}")
        return r.json()
    logging.info(f"Message not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()


def send_template(self, template: str, recipient_id: str, components: str, lang: str = "en_US"):
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
        components[list]: List of components to be sent to the user  # CHANGE
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_template("hello_world", "5511999999999", lang="en_US"))
    """
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
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Template sent to {recipient_id}")
        return r.json()
    logging.info(f"Template not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()


def mark_as_read(self, message_id: str) -> Dict[Any, Any]:
    """
    Marks a message as read

    Args:
        message_id[str]: Id of the message to be marked as read

    Returns:
        Dict[Any, Any]: Response from the API

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.mark_as_read("message_id")
    """
    headers = {
        "Authorization": f"Bearer {self.token}",
        "Content-Type": "application/json",
    }

    json_data = {
        "messaging_product": "whatsapp",
        "status": "read",
        "message_id": message_id,
    }
    logging.info(f"Marking message {message_id} as read")
    response = requests.post(
        f"{self.base_url}/{self.phone_number_id}/messages",
        headers=headers,
        json=json_data,
    ).json()
    if response.status_code == 200:
        logging.info(f"Message {message_id} marked as read")
        return response
    logging.info(f"Error marking message {message_id} as read")
    logging.info(f"Status code: {response.status_code}")
    logging.info(f"Response: {response.json()}")
    return response
