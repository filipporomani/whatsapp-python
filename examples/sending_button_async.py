from os import getenv
from whatsapp import AsyncWhatsApp, AsyncMessage
import asyncio
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = AsyncWhatsApp(token=getenv("TOKEN"), phone_number_id={1: "1234", 2: "5678"})

    async def run_test():
        response = await messenger.send_button(
            recipient_id="255757xxxxxx",
            button={
                "header": "Header Testing",
                "body": "Body Testing",
                "footer": "Footer Testing",
                "action": {
                    "button": "Button Testing",
                    "sections": [
                        {
                            "title": "iBank",
                            "rows": [
                                {"id": "row 1", "title": "Send Money", "description": ""},
                                {
                                    "id": "row 2",
                                    "title": "Withdraw money",
                                    "description": "",
                                },
                            ],
                        }
                    ],
                },
            },
            sender=1,
        )
        while not response.done():
            await asyncio.sleep(.1)
        print(response.result())
        
    asyncio.run(run_test())
