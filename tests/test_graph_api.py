from unittest.mock import Mock, patch

import pytest

from whatsapp.constants import DEFAULT_GRAPH_API_VERSION
from whatsapp.graph_api import (
    normalize_graph_api_version,
    resolve_graph_api_version,
)


def test_normalize_graph_api_version():
    assert normalize_graph_api_version("v27.0") == "v27.0"
    assert normalize_graph_api_version("27.0") == "v27.0"
    assert normalize_graph_api_version(" latest ") == "latest"
    with pytest.raises(ValueError):
        normalize_graph_api_version("not-a-version")


def test_resolve_explicit_version_skips_network():
    with patch("whatsapp.graph_api.requests.get") as get:
        assert resolve_graph_api_version("v25.0") == "v25.0"
        get.assert_not_called()


def test_resolve_latest_from_labeled_table():
    html = """
    <html><body>
      <table><tr><td>The latest Graph API version is:</td><td>v27.0</td></tr></table>
    </body></html>
    """
    response = Mock()
    response.text = html
    response.raise_for_status = Mock()
    with patch("whatsapp.graph_api.requests.get", return_value=response) as get:
        assert resolve_graph_api_version("latest") == "v27.0"
        assert get.call_count == 1


def test_resolve_latest_falls_back_when_pages_fail():
    with patch(
        "whatsapp.graph_api.requests.get", side_effect=RuntimeError("offline")
    ):
        assert resolve_graph_api_version("latest") == DEFAULT_GRAPH_API_VERSION


def test_resolve_latest_from_version_list_when_label_missing():
    html = """
    <html><body>
      <table>
        <tr><td>v26.0</td><td>July 29, 2026</td><td>TBD</td></tr>
        <tr><td>v25.0</td><td>February 18, 2026</td><td>TBD</td></tr>
      </table>
    </body></html>
    """
    response = Mock()
    response.text = html
    response.raise_for_status = Mock()
    with patch("whatsapp.graph_api.requests.get", return_value=response):
        assert resolve_graph_api_version("latest") == "v26.0"
