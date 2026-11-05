from whatsapp.ext._static import (
    changed_field,
    get_author,
    get_delivery,
    get_interactive_response,
    get_message,
    get_message_id,
    get_message_type,
    get_mobile,
    get_name,
    get_reaction,
    is_message,
)


SAMPLE_TEXT = {
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
                                "id": "wamid.TEXT",
                                "timestamp": "1700000000",
                                "type": "text",
                                "text": {"body": "hello"},
                            }
                        ],
                    },
                }
            ]
        }
    ]
}

SAMPLE_REACTION = {
    "entry": [
        {
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "messages": [
                            {
                                "from": "15551234567",
                                "id": "wamid.REACT",
                                "timestamp": "1700000001",
                                "type": "reaction",
                                "reaction": {
                                    "message_id": "wamid.TEXT",
                                    "emoji": "👍",
                                },
                            }
                        ]
                    },
                }
            ]
        }
    ]
}

SAMPLE_STATUS = {
    "entry": [
        {
            "changes": [
                {
                    "field": "messages",
                    "value": {
                        "statuses": [
                            {
                                "id": "wamid.OUT",
                                "status": "played",
                                "timestamp": "1700000002",
                            }
                        ]
                    },
                }
            ]
        }
    ]
}


def test_text_message_parsers():
    assert is_message(SAMPLE_TEXT) is True
    assert changed_field(SAMPLE_TEXT) == "messages"
    assert get_mobile(SAMPLE_TEXT) == "15551234567"
    assert get_name(SAMPLE_TEXT) == "Ada"
    assert get_author(SAMPLE_TEXT) == "15551234567"
    assert get_message(SAMPLE_TEXT) == "hello"
    assert get_message_id(SAMPLE_TEXT) == "wamid.TEXT"
    assert get_message_type(SAMPLE_TEXT) == "text"
    assert get_interactive_response(SAMPLE_TEXT) is None


def test_reaction_parser():
    assert get_message_type(SAMPLE_REACTION) == "reaction"
    assert get_reaction(SAMPLE_REACTION) == {
        "message_id": "wamid.TEXT",
        "emoji": "👍",
    }


def test_delivery_status_parser():
    assert is_message(SAMPLE_STATUS) is False
    assert get_delivery(SAMPLE_STATUS) == "played"
