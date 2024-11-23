from os import getenv
from whatsapp import AsyncWhatsApp, AsyncMessage
import asyncio
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = AsyncWhatsApp(token=getenv("TOKEN"), phone_number_id={1: "1234", 2: "5678"})

    msg = AsyncMessage(
        instance=messenger, content="Hello World!", to="919999999999", sender=1
    )
    async def run_test():
        response = await msg.send()
        while not response.done():
            await asyncio.sleep(.1)
        print(response.result())
        
    asyncio.run(run_test())
