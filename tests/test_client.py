import json
from unittest.mock import Mock, patch

import pytest
from fastapi.testclient import TestClient

from whatsapp import AsyncMessage, AsyncWhatsApp, Message, WhatsApp
from whatsapp.errors import InvalidParameterException


def _make_client(cls=WhatsApp, **overrides):
    kwargs = {
        "token": "test-token",
        "phone_number_id": {1: "123456789"},
        "update_check": False,
        "version": "v27.0",
        "verify_token": "verify-me",
        "logger": False,
        "debug": False,
    }
    kwargs.update(overrides)
    with patch("whatsapp.graph_api.requests.get") as discover:
        discover.side_effect = AssertionError("should not discover for pinned version")
        return cls(**kwargs)


def test_init_requires_dict_phone_number_id():
    with pytest.raises(ValueError, match="dictionary"):
        WhatsApp(token="x", phone_number_id="123", update_check=False, version="v27.0")


def test_pinned_version_sets_urls():
    app = _make_client()
    assert app.LATEST == "v27.0"
    assert app.base_url == "https://graph.facebook.com/v27.0"
    assert app.url == "https://graph.facebook.com/v27.0/123456789/messages"
    assert app.VERSION == "4.5.0"


def test_create_message_and_send_payload():
    app = _make_client()
    msg = app.create_message(to="15550001111", content="hi there")
    assert isinstance(msg, Message)

    response = Mock()
    response.status_code = 200
    response.json.return_value = {"messages": [{"id": "wamid.1"}]}
    with patch("whatsapp.requests.post", return_value=response) as post:
        result = msg.send(sender=1)
        assert result["messages"][0]["id"] == "wamid.1"
        args, kwargs = post.call_args
        assert args[0] == "https://graph.facebook.com/v27.0/123456789/messages"
        assert kwargs["json"]["text"]["body"] == "hi there"


def test_mark_as_read_with_typing_indicator():
    app = _make_client()
    inbound = {
        "entry": [
            {
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "contacts": [
                                {
                                    "wa_id": "15551234567",
                                    "profile": {"name": "Ada"},
                                }
                            ],
                            "messages": [
                                {
                                    "from": "15551234567",
                                    "id": "wamid.IN",
                                    "timestamp": "1",
                                    "type": "text",
                                    "text": {"body": "ping"},
                                }
                            ],
                        },
                    }
                ]
            }
        ]
    }
    msg = app.create_message(data=inbound)
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"success": True}
    with patch("whatsapp.requests.post", return_value=response) as post:
        assert msg.show_typing() == {"success": True}
        payload = post.call_args.kwargs["json"]
        assert payload == {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": "wamid.IN",
            "typing_indicator": {"type": "text"},
        }


def test_send_cta_url_and_location_request_payloads():
    app = _make_client()
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"messages": [{"id": "wamid.x"}]}

    with patch("whatsapp.ext._buttons.requests.post", return_value=response) as post:
        app.send_cta_url(
            body="Open our site",
            display_text="Visit",
            url="https://example.com",
            recipient_id="15550001111",
            header="Hello",
            footer="Thanks",
            sender=1,
        )
        cta = post.call_args.kwargs["json"]["interactive"]
        assert cta["type"] == "cta_url"
        assert cta["action"]["parameters"]["url"] == "https://example.com"
        assert cta["header"]["text"] == "Hello"

        app.send_location_request(
            body="Share your location",
            recipient_id="15550001111",
            sender=1,
        )
        location = post.call_args.kwargs["json"]["interactive"]
        assert location["type"] == "location_request_message"
        assert location["action"]["name"] == "send_location"


def test_send_audio_voice_and_document_filename():
    app = _make_client()
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"messages": [{"id": "wamid.media"}]}

    with patch("whatsapp.ext._send_media.requests.post", return_value=response) as post:
        app.send_audio("media-id", "15550001111", link=False, voice=True, sender=1)
        audio = post.call_args.kwargs["json"]["audio"]
        assert audio == {"id": "media-id", "voice": True}

        app.send_document(
            "https://example.com/a.pdf",
            "15550001111",
            caption="Invoice",
            filename="invoice.pdf",
            sender=1,
        )
        document = post.call_args.kwargs["json"]["document"]
        assert document["filename"] == "invoice.pdf"
        assert document["caption"] == "Invoice"
        assert document["link"] == "https://example.com/a.pdf"


def test_send_template_omits_null_components():
    app = _make_client()
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"messages": [{"id": "wamid.t"}]}
    with patch("whatsapp.ext._message.requests.post", return_value=response) as post:
        app.send_template("hello_world", "15550001111", sender=1)
        template = post.call_args.kwargs["json"]["template"]
        assert template == {
            "name": "hello_world",
            "language": {"code": "en_US"},
        }
        assert "components" not in template


def test_error_handle_raises_typed_exception():
    app = _make_client(cls=AsyncWhatsApp)
    with pytest.raises(InvalidParameterException):
        app.handle(
            {
                "error": {
                    "message": "Invalid parameter",
                    "code": 100,
                }
            }
        )


def test_webhook_verification_and_message_dispatch():
    app = _make_client()
    received = {}

    async def on_message(msg):
        received["msg"] = msg

    app.on_message(on_message)
    client = TestClient(app.app)

    ok = client.get("/", params={"hub.verify_token": "verify-me", "hub.challenge": "42"})
    assert ok.status_code == 200
    assert ok.json() == 42

    bad = client.get("/", params={"hub.verify_token": "nope", "hub.challenge": "42"})
    assert bad.status_code == 200
    assert bad.json() == {"success": False}

    payload = {
        "entry": [
            {
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "contacts": [
                                {
                                    "wa_id": "15551234567",
                                    "profile": {"name": "Ada"},
                                }
                            ],
                            "messages": [
                                {
                                    "from": "15551234567",
                                    "id": "wamid.IN",
                                    "timestamp": "1",
                                    "type": "text",
                                    "text": {"body": "ping"},
                                }
                            ],
                        },
                    }
                ]
            }
        ]
    }
    posted = client.post("/", content=json.dumps(payload))
    assert posted.status_code == 200
    assert posted.json() == {"success": True}
    assert isinstance(received["msg"], Message)
    assert received["msg"].content == "ping"
    assert received["msg"].sender == "15551234567"


def test_async_client_creates_async_message():
    app = _make_client(cls=AsyncWhatsApp)
    msg = app.create_message(to="15550001111", content="async hi")
    assert isinstance(msg, AsyncMessage)
