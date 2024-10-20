from whatsapp import WhatsApp, Message
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("GRAPH_API_TOKEN")
phone_number_id = {1: getenv("TEST_PHONE_NUMBER_ID")}
dest_phone_number = getenv("DEST_PHONE_NUMBER")

app = WhatsApp(token=token, phone_number_id=phone_number_id,
               update_check=False)
msg = app.create_message(to=dest_phone_number, content="Hello world")


# test every single method and print the result
print("Testing send_text")
msg.send(sender=1)

print("Testing send_reply_button")
v = app.send_reply_button(
    button={
        "type": "button",
        "body": {
                "text": "This is a test button"
        },
        "action": {
            "buttons": [
                {
                    "type": "reply",
                    "reply": {
                            "id": "b1",
                            "title": "This is button 1"
                    }
                },
                {
                    "type": "reply",
                    "reply": {
                            "id": "b2",
                            "title": "this is button 2"
                    }
                }
            ]
        }
    },
    recipient_id=dest_phone_number,
    sender=1

)
print(f"send_reply_button: {v}")


print("Creating button")
v = app.create_button(
    button={
        "header": {
            "type": "text",
            "text": "your-header-content"
        },
        "body": {
            "text": "your-text-message-content"
        },
        "footer": {
            "text": "your-footer-content"
        },
        "action": {
            "button": "cta-button-content",
            "sections": [
                {
                    "title": "your-section-title-content",
                    "rows": [
                        {
                            "id": "unique-row-identifier",
                            "title": "row-title-content",
                            "description": "row-description-content",
                        }
                    ]
                },
            ]
        }
    },
)
print(f"create_button: {v}")
print("sending button")
v = app.send_button({
    "header": "Header Testing",
    "body": "Body Testing",
    "footer": "Footer Testing",
    "action": {
        "button": "cta-button-content",
        "sections": [
            {
                "title": "your-secti",
                "rows": [
                    {
                        "id": "unique-row-",
                        "title": "row-title-",
                        "description": "row-description-",
                    }
                ]
            },
        ]
    }
}, dest_phone_number, sender=1)
print(f"send_button: {v}")
print("sending image")
v = app.send_image(
    "https://file-examples.com/storage/feb05093336710053a32bc1/2017/10/file_example_JPG_1MB.jpg", dest_phone_number, sender=1)
print(f"send_image: {v}")
print("sending video")
v = app.send_video(
    "https://file-examples.com/storage/feb05093336710053a32bc1/2017/04/file_example_MP4_480_1_5MG.mp4", dest_phone_number, sender=1)
print(f"send_video: {v}")
print("sending audio")
v = app.send_audio(
    "https://file-examples.com/storage/feb05093336710053a32bc1/2017/11/file_example_MP3_1MG.mp3", dest_phone_number, sender=1)
print(f"send_audio: {v}")
print("sending document")
v = app.send_document(
    "https://file-examples.com/storage/feb05093336710053a32bc1/2017/10/file-example_PDF_1MB.pdf", dest_phone_number, sender=1)
print(f"send_document: {v}")
print("sending location")
v = app.send_location("37.7749", "-122.4194", "test",
                      "test, test", dest_phone_number, sender=1)
print(f"send_location: {v}")
print("sending template")
v = app.send_template(
    "hello_world", dest_phone_number, sender=1)
print(f"send_template: {v}") # this returns error if the phone number is not a test phone number