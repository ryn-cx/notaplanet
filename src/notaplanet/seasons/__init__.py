# TODO: Validate
"""Contains the Seasons class."""

from __future__ import annotations

from http import HTTPStatus
from logging import NullHandler, getLogger
from typing import Any, override

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.exceptions import (
    PageOutOfRangeError,
    ResourceNotFoundError,
    SeriesNotFoundError,
)
from notaplanet.seasons.models import SeasonsModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())

OFFSET = 1000
"""Number of seasons per page. The web player asks for a number high enough that
every season of every series fits on a single page."""


class Seasons(BaseEndpoint[SeasonsModel]):
    """Manage the seasons file.

    The response contains the series metadata, its seasons, and every episode of
    those seasons.

    Source: https://pluto.tv/on-demand/series/{series_id}/details

    Example request:
        - GET /v4/vod/series/{series_id}/seasons?
            - offset=1000&
            - page=1
            - HTTP/2
        - Host: service-vod.clusters.pluto.tv
        - User-Agent: __REDACTED__
        - Accept: */*
        - Accept-Language: en-US,en;q=0.9
        - Accept-Encoding: gzip, deflate, br, zstd
        - Referer: https://pluto.tv/
        - Authorization: Bearer __REDACTED__
        - Origin: https://pluto.tv
        - Connection: keep-alive
        - Sec-Fetch-Dest: empty
        - Sec-Fetch-Mode: cors
        - Sec-Fetch-Site: same-site
        - Priority: u=0
        - TE: trailers
    """

    _response_model = SeasonsModel

    @override
    def download(
        self,
        series_id: str,
        *,
        offset: int = OFFSET,
        page: int = 1,
    ) -> dict[str, Any]:
        log_id = self.get_log_id(self.download, locals())
        try:
            response = self._client.download(
                "vod",
                f"v4/vod/series/{series_id}/seasons",
                params={"offset": offset, "page": page},
                log_id=log_id,
            )
        except ResourceNotFoundError as err:
            raise SeriesNotFoundError(
                series_id,
                err.status_code,
                err.response,
            ) from err
        return self._validate_download(response, series_id, page)

    def _validate_download(
        self,
        response: dict[str, Any],
        series_id: str,
        page: int,
    ) -> dict[str, Any]:
        # An existing series always has at least one season, so an empty list
        # only ever means the requested page is past the last one.
        if not response.get("seasons"):
            if page > 1:
                raise PageOutOfRangeError(page, response)
            raise SeriesNotFoundError(series_id, HTTPStatus.OK, response)
        return response

    @override
    def download_and_parse(
        self,
        series_id: str,
        *,
        offset: int = OFFSET,
        page: int = 1,
    ) -> SeasonsModel:
        return self.parse(self.download(series_id, offset=offset, page=page))
