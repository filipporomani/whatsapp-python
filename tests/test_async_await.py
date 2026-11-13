import asyncio
from unittest.mock import patch

from whatsapp import AsyncWhatsApp


def _client():
    with patch("whatsapp.graph_api.requests.get") as discover:
        discover.side_effect = AssertionError("pinned")
        return AsyncWhatsApp(
            token="t",
            phone_number_id={1: "123"},
            update_check=False,
            version="v27.0",
            logger=False,
            debug=False,
        )


def test_async_send_returns_dict_not_future():
    app = _client()
    msg = app.create_message(to="15550001111", content="hi")

    class Resp:
        status = 200

        async def json(self):
            return {"messages": [{"id": "wamid.1"}]}

    class PostCM:
        async def __aenter__(self):
            return Resp()

        async def __aexit__(self, *a):
            return False

    class Session:
        def post(self, *a, **k):
            return PostCM()

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

    async def run():
        with patch("whatsapp.aiohttp.ClientSession", return_value=Session()):
            return await msg.send(sender=1)

    result = asyncio.run(run())
    assert isinstance(result, dict)
    assert result["messages"][0]["id"] == "wamid.1"
