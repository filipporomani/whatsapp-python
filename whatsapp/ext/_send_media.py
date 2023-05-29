import logging
import requests


def send_location(self, lat: str, long: str, name: str, address: str, recipient_id: str) -> dict:
    """
    Sends a location message to a WhatsApp user

    Args:
        lat[str]: Latitude of the location
        long[str]: Longitude of the location
        name[str]: Name of the location
        address[str]: Address of the location
        recipient_id[str]: Phone number of the user with country code wihout +

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_location("-23.564", "-46.654", "My Location", "Rua dois, 123", "5511999999999")
    """
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_id,
        "type": "location",
        "location": {
            "latitude": lat,
            "longitude": long,
            "name": name,
            "address": address,
        },
    }
    logging.info(f"Sending location to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Location sent to {recipient_id}")
        return r.json()
    logging.info(f"Location not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(r.json())
    return r.json()


def send_image(
    self,
    image: str,
    recipient_id: str,
    recipient_type: str = "individual",
    caption: str = "",
    link: bool = True,
) -> dict:
    """
    Sends an image message to a WhatsApp user

    There are two ways to send an image message to a user, either by passing the image id or by passing the image link.
    Image id is the id of the image uploaded to the cloud api.

    Args:
        image[str]: Image id or link of the image
        recipient_id[str]: Phone number of the user with country code wihout +
        recipient_type[str]: Type of the recipient, either individual or group
        caption[str]: Caption of the image
        link[bool]: Whether to send an image id or an image link, True means that the image is an id, False means that the image is a link


    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_image("https://i.imgur.com/Fh7XVYY.jpeg", "5511999999999")
    """
    if link:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "image",
            "image": {"link": image, "caption": caption},
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "image",
            "image": {"id": image, "caption": caption},
        }
    logging.info(f"Sending image to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Image sent to {recipient_id}")
        return r.json()
    logging.info(f"Image not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(r.json())
    return r.json()


def send_sticker(self, sticker: str, recipient_id: str, recipient_type: str = "individual", link: bool = True) -> dict:
    """
    Sends a sticker message to a WhatsApp user

    There are two ways to send a sticker message to a user, either by passing the image id or by passing the sticker link.
    Sticker id is the id of the sticker uploaded to the cloud api.

    Args:
        sticker[str]: Sticker id or link of the sticker
        recipient_id[str]: Phone number of the user with country code wihout +
        recipient_type[str]: Type of the recipient, either individual or group
        link[bool]: Whether to send an sticker id or an sticker link, True means that the sticker is an id, False means that the image is a link


    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_sticker("170511049062862", "5511999999999", link=False)
    """
    if link:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "sticker",
            "sticker": {"link": sticker},
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "sticker",
            "sticker": {"id": sticker},
        }
    logging.info(f"Sending sticker to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Sticker sent to {recipient_id}")
        return r.json()
    logging.info(f"Sticker not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(r.json())
    return r.json()


def send_audio(self, audio: str, recipient_id: str, link: bool = True) -> dict:
    """
    Sends an audio message to a WhatsApp user
    Audio messages can either be sent by passing the audio id or by passing the audio link.

    Args:
        audio[str]: Audio id or link of the audio
        recipient_id[str]: Phone number of the user with country code wihout +
        link[bool]: Whether to send an audio id or an audio link, True means that the audio is an id, False means that the audio is a link

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", "5511999999999")
    """
    if link:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "audio",
            "audio": {"link": audio},
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "audio",
            "audio": {"id": audio},
        }
    logging.info(f"Sending audio to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Audio sent to {recipient_id}")
        return r.json()
    logging.info(f"Audio not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()


def send_video(
    self, video: str, recipient_id: str, caption: str = "", link: bool = True
) -> dict:
    """ "
    Sends a video message to a WhatsApp user
    Video messages can either be sent by passing the video id or by passing the video link.

    Args:
        video[str]: Video id or link of the video
        recipient_id[str]: Phone number of the user with country code wihout +
        caption[str]: Caption of the video
        link[bool]: Whether to send a video id or a video link, True means that the video is an id, False means that the video is a link

    example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "5511999999999")
    """
    if link:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "video",
            "video": {"link": video, "caption": caption},
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "video",
            "video": {"id": video, "caption": caption},
        }
    logging.info(f"Sending video to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Video sent to {recipient_id}")
        return r.json()
    logging.info(f"Video not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()


def send_document(
    self, document: str, recipient_id: str, caption: str = "", link: bool = True
) -> dict:
    """ "
    Sends a document message to a WhatsApp user
    Document messages can either be sent by passing the document id or by passing the document link.

    Args:
        document[str]: Document id or link of the document
        recipient_id[str]: Phone number of the user with country code wihout +
        caption[str]: Caption of the document
        link[bool]: Whether to send a document id or a document link, True means that the document is an id, False means that the document is a link

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.send_document("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "5511999999999")
    """
    if link:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "document",
            "document": {"link": document, "caption": caption},
        }
    else:
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "document",
            "document": {"id": document, "caption": caption},
        }

    logging.info(f"Sending document to {recipient_id}")
    r = requests.post(self.url, headers=self.headers, json=data)
    if r.status_code == 200:
        logging.info(f"Document sent to {recipient_id}")
        return r.json()
    logging.info(f"Document not sent to {recipient_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.error(f"Response: {r.json()}")
    return r.json()
