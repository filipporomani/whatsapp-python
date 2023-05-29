import logging
import requests


def send_template(self, template: str, recipient_id: str, components: str, lang: str = "en_US") -> dict:
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


# MESSAGE()

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


def send(self, preview_url: bool = True) -> dict:
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": self.rec,
        "to": self.to,
        "type": "text",
        "text": {"preview_url": preview_url, "body": self.content},
    }
    logging.info(f"Sending message to {self.to}")
    r = requests.post(f"{self.url}", headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Message sent to {self.to}")
        return r.json()
    logging.info(f"Message not sent to {self.to}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()
