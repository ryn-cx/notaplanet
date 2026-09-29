# TODO: Validate
"""Contains the Carousel class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger
from typing import Any
from urllib.parse import quote

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.carousel.models import CarouselModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

ROWS = 1000
"""The most titles a carousel lists, however many are asked for."""

QUERY = """
query GetHybridCarouselData($carouselParams: CarouselParams!, $token: String!) {
    carouselData(carouselParams: $carouselParams, token: $token) {
        success
        result {
            id
            title
            total
            rows
            skipped
            hasMore
            data {
                contentType
                href
                id
                thumb
                tileType
                orientation
                ... on ShowCarouselItem {
                    title
                    description
                    genre
                    rating
                    numSeasons
                    premiereDate
                    isKidsContent
                    thumbLandscape
                }
                ... on MovieCarouselItem {
                    title
                    description
                    genre
                    movieId
                    movieDuration
                    airDate
                    isKidsContent
                    thumbLandscape
                }
            }
        }
    }
}
"""


# TODO: Validate
def extract_carousel(response: str) -> dict[str, Any]:
    """Extract the carousel from the GraphQL response."""
    return json.loads(response)["data"]["carouselData"]


# TODO: Validate
class Carousel(BaseEndpoint):
    """Contains the shows and movies one carousel of a hub lists.

    A carousel is read by the token and the model `Hub` carries for it. No
    carousel lists more than 1,000 titles, so the All Shows and All Movies grids
    stop partway through the alphabet.

    A show is listed by its slug and a movie by its id, and `Items` accepts both.

    Source: https://pluto.tv/us/shows/category/all-shows/

    Example request:
        - POST /api/tn/hubs/graphql/
        - Host: pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Body: {"query": "query GetHybridCarouselData(...) {...}", "variables": {...}}
    """

    # TODO: Validate
    def __call__(
        self,
        token: str,
        *,
        model: str,
        start: int = 0,
        rows: int = ROWS,
    ) -> CarouselModel:
        """Download and parse the carousel file."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(
            self.download(token, model=model, start=start, rows=rows),
            log_id,
        )

    # TODO: Validate
    def download(
        self,
        token: str,
        *,
        model: str,
        start: int = 0,
        rows: int = ROWS,
    ) -> str:
        """Download the carousel file."""
        log_id = self.get_log_id(self.download, locals())
        return self._client.download_graphql(
            QUERY,
            {
                "carouselParams": {
                    "model": model,
                    "start": str(start),
                    "rows": str(rows),
                },
                "token": quote(token, safe=""),
            },
            log_id,
        )

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> CarouselModel:
        """Load a carousel file into its model."""
        return model_validate_json(
            extract_carousel(data),
            log_id or self.default_log_id,
        )
