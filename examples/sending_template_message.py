from os import getenv
from whatsapp import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"),
                         phone_number_id={1:"1234", 2: "5678"})

    response = messenger.send_template(
        "hello_world", "255757xxxxxx", components=[], lang="en_US", sender=1)

    print(response)
