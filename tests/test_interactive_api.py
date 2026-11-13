from unittest.mock import Mock, patch

import pytest

from whatsapp import WhatsApp
from whatsapp.errors import InvalidParameterException


def _client():
    with patch("whatsapp.graph_api.requests.get") as discover:
        discover.side_effect = AssertionError("pinned version")
        return WhatsApp(
            token="test-token",
            phone_number_id={1: "123456789"},
            update_check=False,
            version="v27.0",
            logger=False,
            debug=False,
        )


def test_create_button_accepts_string_or_mapping():
    app = _client()
    as_strings = app.create_button(
        {"header": "H", "body": "B", "footer": "F", "action": {"button": "Open"}}
    )
    assert as_strings["header"] == {"type": "text", "text": "H"}
    assert as_strings["body"] == {"text": "B"}
    assert as_strings["footer"] == {"text": "F"}

    as_maps = app.create_button(
        {
            "header": {"type": "text", "text": "H"},
            "body": {"text": "B"},
            "footer": {"text": "F"},
            "action": {"button": "Open"},
        }
    )
    assert as_maps["header"] == {"type": "text", "text": "H"}
    assert as_maps["body"] == {"text": "B"}
    assert as_maps["footer"] == {"text": "F"}


def test_send_flow_payload_and_validation():
    app = _client()
    response = Mock(status_code=200)
    response.json.return_value = {"messages": [{"id": "wamid.flow"}]}

    with pytest.raises(ValueError, match="exactly one"):
        app.send_flow("body", "15550001111", "Open", sender=1)

    with patch("whatsapp.ext._interactive.requests.post", return_value=response) as post:
        app.send_flow(
            "Book a slot",
            "15550001111",
            "Book",
            flow_id="123",
            flow_token="tok",
            header="Appointments",
            sender=1,
        )
        interactive = post.call_args.kwargs["json"]["interactive"]
        assert interactive["type"] == "flow"
        assert interactive["action"]["name"] == "flow"
        assert interactive["action"]["parameters"]["flow_id"] == "123"
        assert interactive["action"]["parameters"]["flow_cta"] == "Book"
        assert interactive["header"]["text"] == "Appointments"


def test_commerce_and_address_and_call_permission_payloads():
    app = _client()
    response = Mock(status_code=200)
    response.json.return_value = {"messages": [{"id": "wamid.x"}]}

    with patch("whatsapp.ext._interactive.requests.post", return_value=response) as post:
        app.send_catalog_message(
            "Browse",
            "15550001111",
            thumbnail_product_retailer_id="SKU1",
            sender=1,
        )
        assert post.call_args.kwargs["json"]["interactive"]["type"] == "catalog_message"

        app.send_product(
            "15550001111",
            catalog_id="CAT",
            product_retailer_id="SKU1",
            body="Nice item",
            sender=1,
        )
        product = post.call_args.kwargs["json"]["interactive"]
        assert product["type"] == "product"
        assert product["action"]["catalog_id"] == "CAT"

        app.send_product_list(
            "15550001111",
            catalog_id="CAT",
            header="Bestsellers",
            body="Pick one",
            sections=[
                {
                    "title": "Popular",
                    "product_items": [{"product_retailer_id": "SKU1"}],
                }
            ],
            sender=1,
        )
        product_list = post.call_args.kwargs["json"]["interactive"]
        assert product_list["type"] == "product_list"
        assert product_list["header"]["type"] == "text"

        app.send_address_message(
            "Where should we deliver?",
            "15550001111",
            country="IN",
            sender=1,
        )
        address = post.call_args.kwargs["json"]["interactive"]
        assert address["type"] == "address_message"
        assert address["action"]["parameters"]["country"] == "IN"

        app.send_call_permission_request(
            "15550001111",
            body="Can we call you?",
            sender=1,
        )
        call = post.call_args.kwargs["json"]["interactive"]
        assert call["type"] == "call_permission_request"
        assert call["action"]["name"] == "call_permission_request"


def test_message_send_raises_typed_errors():
    app = _client()
    msg = app.create_message(to="15550001111", content="hi")
    response = Mock(status_code=400)
    response.json.return_value = {"error": {"message": "Invalid parameter", "code": 100}}
    with patch("whatsapp.requests.post", return_value=response):
        with pytest.raises(InvalidParameterException):
            msg.send(sender=1)
