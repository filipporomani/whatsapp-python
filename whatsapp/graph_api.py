"""Helpers for resolving the Meta Graph API version used by WhatsApp Cloud API."""

from __future__ import annotations

import logging
import re
from typing import Iterable, Optional

import requests
from bs4 import BeautifulSoup

from .constants import DEFAULT_GRAPH_API_VERSION

CHANGELOG_URLS: tuple[str, ...] = (
    "https://developers.facebook.com/docs/graph-api/changelog/",
    "https://developers.facebook.com/docs/graph-api/changelog/versions/",
)

_VERSION_RE = re.compile(r"v\d+\.\d+")
_LATEST_LABEL = "the latest graph api version is"


def normalize_graph_api_version(version: str) -> str:
    """Normalize a Graph API version string to the ``vX.Y`` form."""
    cleaned = (version or "").strip()
    if not cleaned:
        raise ValueError("Graph API version must be a non-empty string")
    if cleaned.lower() == "latest":
        return "latest"
    if not cleaned.startswith("v"):
        cleaned = f"v{cleaned}"
    if not _VERSION_RE.fullmatch(cleaned):
        raise ValueError(f"Invalid Graph API version: {version!r}")
    return cleaned


def _version_sort_key(version: str) -> tuple[int, int]:
    major, minor = version[1:].split(".")
    return int(major), int(minor)


def _extract_latest_from_tables(soup: BeautifulSoup) -> Optional[str]:
    for table in soup.find_all("table"):
        for row in table.find_all("tr"):
            cells = [
                "".join(cell.stripped_strings).strip()
                for cell in row.find_all(["td", "th"])
            ]
            if not cells:
                continue
            joined = " ".join(cells).lower()
            if _LATEST_LABEL in joined:
                for cell in cells:
                    match = _VERSION_RE.search(cell)
                    if match:
                        return match.group(0)
    return None


def _extract_versions(text: str) -> list[str]:
    return sorted(set(_VERSION_RE.findall(text)), key=_version_sort_key, reverse=True)


def _fetch_latest_from_url(url: str, timeout: float) -> Optional[str]:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "whatsapp-python/graph-api-version-check"},
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    labeled = _extract_latest_from_tables(soup)
    if labeled:
        return labeled
    versions = _extract_versions(response.text)
    return versions[0] if versions else None


def resolve_graph_api_version(
    version: str = "latest",
    *,
    timeout: float = 10.0,
    urls: Optional[Iterable[str]] = None,
) -> str:
    """
    Resolve the Graph API version to use for Cloud API requests.

    ``version="latest"`` scrapes Meta's public changelog pages and falls back to
    :data:`DEFAULT_GRAPH_API_VERSION` when discovery fails.
    """
    normalized = normalize_graph_api_version(version)
    if normalized != "latest":
        return normalized

    errors: list[str] = []
    for url in tuple(urls) if urls is not None else CHANGELOG_URLS:
        try:
            discovered = _fetch_latest_from_url(url, timeout=timeout)
        except Exception as exc:  # noqa: BLE001 - discovery must never break init
            errors.append(f"{url}: {exc}")
            continue
        if discovered:
            return discovered
        errors.append(f"{url}: no version found")

    if errors:
        logging.warning(
            "Unable to discover the latest Graph API version (%s); "
            "falling back to %s",
            "; ".join(errors),
            DEFAULT_GRAPH_API_VERSION,
        )
    return DEFAULT_GRAPH_API_VERSION
