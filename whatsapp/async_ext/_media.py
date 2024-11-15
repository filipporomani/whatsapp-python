import logging
import aiohttp
import asyncio
import os
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Union, Dict, Any


async def upload_media(self, media: str, sender=None) -> asyncio.Future:
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
    try:
        sender = dict(self.l)[sender]

    except:
        sender = self.phone_number_id

    if sender == None:
        sender = self.phone_number_id

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
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://graph.facebook.com/{self.LATEST}/{sender}/media",
                headers=headers,
                data=form_data,
            ) as r:
                if r.status == 200:
                    logging.info(f"Media {media} uploaded")
                    return await r.json()
                logging.info(f"Error uploading media {media}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f



async def delete_media(self, media_id: str) -> asyncio.Future:
    """
    Deletes a media from the cloud api

    Args:
        media_id[str]: Id of the media to be deleted
    """
    logging.info(f"Deleting media {media_id}")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"https://graph.facebook.com/{self.LATEST}/{media_id}",
                headers=self.headers,
            ) as r:
                if r.status == 200:
                    logging.info(f"Media {media_id} deleted")
                    return await r.json()
                logging.info(f"Error deleting media {media_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f


async def query_media_url(self, media_id: str) -> asyncio.Future:
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
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://graph.facebook.com/{self.LATEST}/{media_id}",
                headers=self.headers,
            ) as r:
                if r.status == 200:
                    logging.info(f"Media url for {media_id} queried")
                    return await r.json()
                logging.info(f"Error querying media url for {media_id}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f



async def download_media(
    self, media_url: str, mime_type: str, file_path: str = "temp"
) -> asyncio.Future:
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
    logging.info(f"Downloading media from {media_url}")
    async def call():
        async with aiohttp.ClientSession() as session:
            async with session.get(media_url, headers=self.headers) as r:
                if r.status == 200:
                    logging.info(f"Media downloaded from {media_url}")
                    extension = mime_type.split("/")[1]
                    save_file_here = (
                        f"{file_path}.{extension}" if file_path else f"temp.{extension}"
                    )
                    with open(save_file_here, "wb") as f:
                        f.write(await r.read())
                    return save_file_here
                logging.info(f"Error downloading media from {media_url}")
                logging.info(f"Status code: {r.status}")
                logging.info(f"Response: {await r.json()}")
                return await r.json()
    f = asyncio.ensure_future(call())
    await asyncio.sleep(.001) # make asyncio run the task
    return f