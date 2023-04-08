from os import getenv
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("ID"))

    data = {"your": "data"}

    msg = Message(data=data, instance=messenger)
    msg.reply("lol")

    print(msg)
