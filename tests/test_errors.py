import pytest

from whatsapp.errors import (
    DisplayNameApprovalException,
    Handle,
    MarketingOptOutException,
    TemplateClassificationLimitException,
)


@pytest.mark.parametrize(
    "code,exc",
    [
        (131037, DisplayNameApprovalException),
        (131050, MarketingOptOutException),
        (131064, TemplateClassificationLimitException),
    ],
)
def test_new_error_mappings(code, exc):
    with pytest.raises(exc):
        Handle({"error": {"message": "boom", "code": code}})


def test_unknown_error_falls_back_to_handler():
    from whatsapp.errors import Handler

    with pytest.raises(Handler):
        Handle({"error": {"message": "mystery", "code": 999999}})
