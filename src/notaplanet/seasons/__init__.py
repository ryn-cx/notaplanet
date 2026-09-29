# TODO: Validate
"""Contains the Seasons class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.exceptions import (
    ResourceNotFoundError,
    SeriesNotFoundError,
    WrongSeriesError,
)
from notaplanet.seasons.models import SeasonsModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

OFFSET = 1000
"""Number of seasons per page, high enough that every series fits on one page."""


# TODO: Validate
class Seasons(BaseEndpoint):
    """Contains the seasons.

    Every season of one series, with its episodes. A page past the last one is
    answered with the series and no seasons.

    Source: https://pluto.tv/on-demand/series/{series_id}/details

    Example request:
        - GET /v4/vod/series/{series_id}/seasons?
            - offset=1000&
            - page=1
        - Host: service-vod.clusters.pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Authorization: Bearer __REDACTED__
    """

    # TODO: Validate
    def __call__(
        self,
        series_id: str,
        *,
        offset: int = OFFSET,
        page: int = 1,
    ) -> SeasonsModel:
        """Download and parse the seasons file."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(series_id, offset=offset, page=page), log_id)

    # TODO: Validate
    def download(
        self,
        series_id: str,
        *,
        offset: int = OFFSET,
        page: int = 1,
    ) -> str:
        """Download the seasons file."""
        log_id = self.get_log_id(self.download, locals())
        try:
            response = self._client.download(
                "vod",
                f"v4/vod/series/{series_id}/seasons",
                {"offset": offset, "page": page},
                log_id,
            )
        except ResourceNotFoundError as err:
            raise SeriesNotFoundError(
                series_id,
                err.status_code,
                err.response,
            ) from err
        return self._validate_download(response, series_id)

    # TODO: Validate
    def _validate_download(self, response: str, series_id: str) -> str:
        if json.loads(response).get("_id") != series_id:
            raise WrongSeriesError(series_id, response)
        return response

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> SeasonsModel:
        """Load a seasons file into its model."""
        return model_validate_json(data, log_id or self.default_log_id)
