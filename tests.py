from whatsapp import WhatsApp
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("GRAPH_API_TOKEN")
phone_number_id = {1: getenv("TEST_PHONE_NUMBER_ID")}

app = WhatsApp(token=token, phone_number_id=phone_number_id, update_check=False)
