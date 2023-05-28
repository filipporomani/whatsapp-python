import os
import logging
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv
from flask import Flask, request, Response

# Initialize Flask App
app = Flask(__name__)

# Load .env file
load_dotenv("../.env")
messenger = WhatsApp(os.getenv("TOKEN"),
                     phone_number_id=os.getenv("ID"))
VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"

# Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@app.get("/")
def verify_token():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        logging.info("Verified webhook")
        challenge = request.args.get("hub.challenge")
        return str(challenge)
    logging.error("Webhook Verification failed")
    return "Invalid verification token"


@app.post("/")
def hook():
    # Handle Webhook Subscriptions
    data = request.get_json()
    if data is None:
        return Response(status=200)
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.is_message(data)
        if new_message:
            msg = Message(instance=messenger, data=data)
            mobile = msg.sender
            name = msg.name
            message_type = msg.type
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = msg.content
                name = msg.name
                logging.info("Message: %s", message)
                m = Message(instance=messenger, to=mobile,
                            content="Hello World")
                m.send()

            elif message_type == "interactive":
                message_response = msg.interactive
                if message_response is None:
                    return Response(status=400)
                interactive_type = message_response.get("type")
                message_id = message_response[interactive_type]["id"]
                message_text = message_response[interactive_type]["title"]
                logging.info(
                    f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = msg.location
                if message_location is None:
                    return Response(status=400)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s",
                             message_latitude, message_longitude)

            elif message_type == "image":
                image = msg.image
                if image is None:
                    return Response(status=400)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                if image_url is None:
                    return Response(status=400)
                image_filename = messenger.download_media(image_url, mime_type)
                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "video":
                video = msg.video
                if video is None:
                    return Response(status=400)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                if video_url is None:
                    return Response(status=400)
                video_filename = messenger.download_media(video_url, mime_type)
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = msg.audio
                if audio is None:
                    return Response(status=400)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                if audio_url is None:
                    return Response(status=400)
                audio_filename = messenger.download_media(audio_url, mime_type)
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "document":
                file = msg.document
                if file is None:
                    return Response(status=400)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                if file_url is None:
                    return Response(status=400)
                file_filename = messenger.download_media(file_url, mime_type)
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                logging.info(f"{mobile} sent {message_type} ")
                logging.info(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                logging.info(f"Message : {delivery}")
            else:
                logging.info("No new message")
    return "OK", 200


if __name__ == "__main__":
    app.run(port=6869, debug=False)
