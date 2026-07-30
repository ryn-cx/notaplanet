# TODO: Validate
"""Exceptions."""

from __future__ import annotations

from typing import Any


class NotAPlanetError(Exception):
    """Base exception for NotAPlanet."""

    response: str | dict[str, Any] | list[Any] | None = None


class HTTPError(NotAPlanetError):
    """Raised when HTTP request fails with unexpected status code."""

    def __init__(
        self,
        status_code: int,
        response: str | dict[str, Any] | list[Any] | None,
    ) -> None:
        """Initialize the HTTPError with the status code and response body."""
        self.status_code = status_code
        self.response = response
        super().__init__(f"Unexpected response status code: {status_code}")


class ResourceNotFoundError(HTTPError):
    """Raised when the API reports that the requested resource does not exist."""


class SeriesNotFoundError(ResourceNotFoundError):
    """Raised when the requested series does not exist."""

    def __init__(
        self,
        series_id: str,
        status_code: int,
        response: str | dict[str, Any] | list[Any] | None,
    ) -> None:
        """Initialize with the series id and the originating response."""
        self.series_id = series_id
        super().__init__(status_code, response)


class ItemNotFoundError(ResourceNotFoundError):
    """Raised when none of the requested items exist."""

    def __init__(
        self,
        item_ids: list[str],
        status_code: int,
        response: str | dict[str, Any] | list[Any] | None,
    ) -> None:
        """Initialize with the requested item ids and the originating response."""
        self.item_ids = item_ids
        super().__init__(status_code, response)


class PageOutOfRangeError(NotAPlanetError, ValueError):
    """Raised when the requested page is past the last page of results."""

    def __init__(self, page: int, response: dict[str, Any]) -> None:
        """Initialize with the requested page and the original response."""
        self.page = page
        self.response = response
        super().__init__(f"Requested page {page} is out of range")


class UnknownServerError(NotAPlanetError, KeyError):
    """Raised when the boot response does not include a requested service host."""

    def __init__(self, server: str, servers: dict[str, str]) -> None:
        """Initialize with the missing server name and the servers that do exist."""
        self.server = server
        self.servers = servers
        super().__init__(f"Boot response has no host for server {server!r}")
