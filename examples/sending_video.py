from os import getenv
from whatsapp import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"),
                         phone_number_id={1:"1234", 2: "5678"})

    response = messenger.send_video(
        video="https://www.youtube.com/watch?v=K4TOrB7at0Y",
        recipient_id="255757xxxxxx",
        sender=1
    )

    print(response)
