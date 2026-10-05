# TODO: Validate
"""Exceptions."""

from __future__ import annotations

from typing import Any


# TODO: Validate
class NotAPlanetError(Exception):
    """Base exception for NotAPlanet."""

    response: str | dict[str, Any] | None = None


# TODO: Validate
class HTTPError(NotAPlanetError):
    """Raised when HTTP request fails with unexpected status code."""

    def __init__(
        self,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize the HTTPError with the status code and response body."""
        self.status_code = status_code
        self.response = response
        super().__init__(f"Unexpected response status code: {status_code}")


# TODO: Validate
class ResourceNotFoundError(HTTPError):
    """Raised when the API reports that the requested resource does not exist."""


# TODO: Validate
class SeriesNotFoundError(ResourceNotFoundError):
    """Raised when the requested series does not exist."""

    def __init__(
        self,
        series_id: str,
        status_code: int,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize with the series id and the originating response."""
        self.series_id = series_id
        super().__init__(status_code, response)


# TODO: Validate
class WrongSeriesError(NotAPlanetError):
    """Raised when the downloaded seasons are for a different series."""

    def __init__(
        self,
        series_id: str,
        response: str | dict[str, Any] | None,
    ) -> None:
        """Initialize with the series id that was asked for and the response."""
        self.series_id = series_id
        self.response = response
        super().__init__(f"The downloaded file is not for series {series_id!r}")


# TODO: Validate
class UnknownServerError(NotAPlanetError, KeyError):
    """Raised when the boot response has no host for the requested service."""

    def __init__(self, server: str, servers: dict[str, str]) -> None:
        """Initialize with the missing server name and the servers that do exist."""
        self.server = server
        self.servers = servers
        self.response = servers
        super().__init__(f"Boot response has no host for server {server!r}")


# TODO: Validate
class GraphQLError(NotAPlanetError):
    """Raised when the hubs GraphQL API answers with errors."""

    # TODO: Validate
    def __init__(self, codes: list[str], response: str) -> None:
        """Initialize with the error codes and the response body."""
        self.codes = codes
        self.response = response
        super().__init__(f"The GraphQL API answered with errors: {codes}")


# TODO: Validate
class HubNotFoundError(NotAPlanetError):
    """Raised when the requested hub does not exist."""

    # TODO: Validate
    def __init__(self, hub_slug: str, response: str | dict[str, Any] | None) -> None:
        """Initialize with the hub slug and the originating response."""
        self.hub_slug = hub_slug
        self.response = response
        super().__init__(f"No hub is filed under {hub_slug!r}")


# TODO: Validate
class ShowNotFoundError(NotAPlanetError):
    """Raised when the requested show does not exist."""

    # TODO: Validate
    def __init__(self, slug: str, response: str | dict[str, Any] | None) -> None:
        """Initialize with the show slug and the originating response."""
        self.slug = slug
        self.response = response
        super().__init__(f"No show is filed under {slug!r}")


# TODO: Validate
class MovieNotFoundError(NotAPlanetError):
    """Raised when the requested movie does not exist."""

    # TODO: Validate
    def __init__(self, movie_id: str, response: str | dict[str, Any] | None) -> None:
        """Initialize with the movie id and the originating response."""
        self.movie_id = movie_id
        self.response = response
        super().__init__(f"No movie is filed under {movie_id!r}")
