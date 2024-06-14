import logging
import requests
import os
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Union, Dict, Any


def upload_media(self, media: str) -> Union[Dict[Any, Any], None]:
    """
    Uploads a media to the cloud api and returns the id of the media

    Args:
        media[str]: Path of the media to be uploaded

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.upload_media("/path/to/media")

    REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#
    """
    form_data = {
        "file": (
            media,
            open(os.path.realpath(media), "rb"),
            mimetypes.guess_type(media)[0],
        ),
        "messaging_product": "whatsapp",
        "type": mimetypes.guess_type(media)[0],
    }
    form_data = MultipartEncoder(fields=form_data)
    headers = self.headers.copy()
    headers["Content-Type"] = form_data.content_type
    logging.info(f"Content-Type: {form_data.content_type}")
    logging.info(f"Uploading media {media}")
    r = requests.post(
        f"{self.base_url}/{self.phone_number_id}/media",
        headers=headers,
        data=form_data,
    )
    if r.status_code == 200:
        logging.info(f"Media {media} uploaded")
        return r.json()
    logging.info(f"Error uploading media {media}")
    logging.info(f"Status code: {r.status_code}")
    logging.debug(f"Response: {r.json()}")
    return None


def delete_media(self, media_id: str) -> Union[Dict[Any, Any], None]:
    """
    Deletes a media from the cloud api

    Args:
        media_id[str]: Id of the media to be deleted
    """
    logging.info(f"Deleting media {media_id}")
    r = requests.delete(
        f"{self.base_url}/{media_id}", headers=self.headers)
    if r.status_code == 200:
        logging.info(f"Media {media_id} deleted")
        return r.json()
    logging.info(f"Error deleting media {media_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return None


def query_media_url(self, media_id: str) -> Union[str, None]:
    """
    Query media url from media id obtained either by manually uploading media or received media

    Args:
        media_id[str]: Media id of the media

    Returns:
        str: Media url

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.query_media_url("media_id")
    """

    logging.info(f"Querying media url for {media_id}")
    r = requests.get(f"{self.base_url}/{media_id}", headers=self.headers)
    if r.status_code == 200:
        logging.info(f"Media url queried for {media_id}")
        return r.json()["url"]
    logging.info(f"Media url not queried for {media_id}")
    logging.info(f"Status code: {r.status_code}")
    logging.info(f"Response: {r.json()}")
    return None


def download_media(
    self, media_url: str, mime_type: str, file_path: str = "temp"
) -> Union[str, None]:
    """
    Download media from media url obtained either by manually uploading media or received media

    Args:
        media_url[str]: Media url of the media
        mime_type[str]: Mime type of the media
        file_path[str]: Path of the file to be downloaded to. Default is "temp"
                        Do not include the file extension. It will be added automatically.

    Returns:
        str: Media url

    Example:
        >>> from whatsapp import WhatsApp
        >>> whatsapp = WhatsApp(token, phone_number_id)
        >>> whatsapp.download_media("media_url", "image/jpeg")
        >>> whatsapp.download_media("media_url", "video/mp4", "path/to/file") #do not include the file extension
    """
    r = requests.get(media_url, headers=self.headers)
    content = r.content
    extension = mime_type.split("/")[1]
    save_file_here = None
    # create a temporary file
    try:

        save_file_here = (
            f"{file_path}.{extension}" if file_path else f"temp.{extension}"
        )
        with open(save_file_here, "wb") as f:
            f.write(content)
        logging.info(f"Media downloaded to {save_file_here}")
        return f.name
    except Exception as e:
        logging.info(e)
        logging.error(f"Error downloading media to {save_file_here}")
        return None
