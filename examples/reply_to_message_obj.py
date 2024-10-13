from os import getenv
from whatsapp import WhatsApp, Message
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id={1:"1234", 2: "5678"})

    data = {"your": "data"}

    msg = Message(data=data, instance=messenger,sender=1)
    msg.reply("lol")

    print(msg)
