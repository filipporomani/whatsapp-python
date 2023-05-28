from os import getenv
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"),
                         phone_number_id=getenv("PHONE_NUMBER_ID"))

    msg = Message(instance=messenger,
                  content="Hello World!", to="919999999999")
    response = msg.send()

    print(response)
