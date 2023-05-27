from typing import Any, Dict, Union


@staticmethod
def is_message(data: Dict[Any, Any]) -> bool:
    """is_message checks if the data received from the webhook is a message.

    Args:
        data (Dict[Any, Any]): The data received from the webhook

    Returns:
        bool: True if the data is a message, False otherwise
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return True
    else:
        return False


@staticmethod
def get_mobile(data: Dict[Any, Any]) -> Union[str, None]:
    """
    Extracts the mobile number of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        str: The mobile number of the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> mobile = whatsapp.get_mobile(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "contacts" in data:
        return data["contacts"][0]["wa_id"]


@staticmethod
def get_name(data: Dict[Any, Any]) -> Union[str, None]:
    """
    Extracts the name of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        str: The name of the sender
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> mobile = whatsapp.get_name(data)
    """
    contact = data["entry"][0]["changes"][0]["value"]
    if contact:
        return contact["contacts"][0]["profile"]["name"]


@staticmethod
def get_message(data: Dict[Any, Any]) -> Union[str, None]:
    """
    Extracts the text message of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        str: The text message received from the sender
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> message = message.get_message(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return data["messages"][0]["text"]["body"]


@staticmethod
def get_message_id(data: Dict[Any, Any]) -> Union[str, None]:
    """
    Extracts the message id of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        str: The message id of the sender
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> message_id = whatsapp.get_message_id(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return data["messages"][0]["id"]


@staticmethod
def get_message_timestamp(data: Dict[Any, Any]) -> Union[str, None]:
    """ "
    Extracts the timestamp of the message from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        str: The timestamp of the message
    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.get_message_timestamp(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return data["messages"][0]["timestamp"]


@staticmethod
def get_interactive_response(data: Dict[Any, Any]) -> Union[Dict, None]:
    """
        Extracts the response of the interactive message from the data received from the webhook.

        Args:
        data[dict]: The data received from the webhook
    Returns:
        dict: The response of the interactive message

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> response = whatsapp.get_interactive_response(data)
        >>> interactive_type = response.get("type")
        >>> message_id = response[interactive_type]["id"]
        >>> message_text = response[interactive_type]["title"]
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        if "interactive" in data["messages"][0]:
            return data["messages"][0]["interactive"]


@staticmethod
def get_location(data: Dict[Any, Any]) -> Union[Dict, None]:
    """
    Extracts the location of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook

    Returns:
        dict: The location of the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.get_location(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        if "location" in data["messages"][0]:
            return data["messages"][0]["location"]


@staticmethod
def get_image(data: Dict[Any, Any]) -> Union[Dict, None]:
    """ "
    Extracts the image of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        dict: The image_id of an image sent by the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> image_id = whatsapp.get_image(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        if "image" in data["messages"][0]:
            return data["messages"][0]["image"]


@staticmethod
def get_document(data: Dict[Any, Any]) -> Union[Dict, None]:
    """ "
    Extracts the document of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook
    Returns:
        dict: The document_id of an image sent by the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> document_id = whatsapp.get_document(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        if "document" in data["messages"][0]:
            return data["messages"][0]["document"]


@staticmethod
def get_audio(data: Dict[Any, Any]) -> Union[Dict, None]:
    """
    Extracts the audio of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook

    Returns:
        dict: The audio of the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.get_audio(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        if "audio" in data["messages"][0]:
            return data["messages"][0]["audio"]


@staticmethod
def get_video(data: Dict[Any, Any]) -> Union[Dict, None]:
    """
    Extracts the video of the sender from the data received from the webhook.

    Args:
        data[dict]: The data received from the webhook

    Returns:
        dict: Dictionary containing the video details sent by the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.get_video(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        if "video" in data["messages"][0]:
            return data["messages"][0]["video"]


@staticmethod
def get_message_type(data: Dict[Any, Any]) -> Union[str, None]:
    """
    Gets the type of the message sent by the sender from the data received from the webhook.


    Args:
        data [dict]: The data received from the webhook

    Returns:
        str: The type of the message sent by the sender

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.get_message_type(data)
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "messages" in data:
        return data["messages"][0]["type"]


@staticmethod
def get_delivery(data: Dict[Any, Any]) -> Union[Dict, None]:
    """
    Extracts the delivery status of the message from the data received from the webhook.
    Args:
        data [dict]: The data received from the webhook

    Returns:
        dict: The delivery status of the message and message id of the message
    """
    data = data["entry"][0]["changes"][0]["value"]
    if "statuses" in data:
        return data["statuses"][0]["status"]


@staticmethod
def changed_field(data: Dict[Any, Any]) -> str:
    """
    Helper function to check if the field changed in the data received from the webhook.

    Args:
        data [dict]: The data received from the webhook

    Returns:
        str: The field changed in the data received from the webhook

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.changed_field(data)
    """
    return data["entry"][0]["changes"][0]["field"]


@staticmethod
def get_author(data: Dict[Any, Any]) -> Union[str, None]:
    try:
        return data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    except Exception:
        return None
