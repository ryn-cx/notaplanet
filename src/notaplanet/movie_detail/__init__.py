# TODO: Validate
"""Contains the MovieDetail class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger
from typing import Any

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.exceptions import MovieNotFoundError
from notaplanet.movie_detail.models import MovieDetailModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

QUERY = """
query MovieHomeData($id: String!) {
    movieDetail(id: $id) {
        movie {
            id
            title
            movieAssets {
                filepath_movie_keep_watching
            }
            logo
            callout
            contentId
            premiereDate
            description
            shortDescription
            longDescription
            genre
            category
            brand
            region
            brandUrl
            numSeasons
            showEpisodeGuideLink
            isLocked
            directors
            pubDate
            seasons {
                seasonNum
                totalCount
            }
            regionalRatings {
                ratingIcon
                rating
                disclaimer
            }
            isKidsContent
        }
        carouselConfigs {
            title
            position
            model
            orientation
            carouselId
            carouselPresentationStyle
            includeVersion
            token
            carouselType
            isContentHighlightEnabled
        }
    }
}
"""


# TODO: Validate
def extract_movie_detail(response: str) -> dict[str, Any] | None:
    """Extract the movie detail from the GraphQL response."""
    return json.loads(response)["data"]["movieDetail"]


# TODO: Validate
class MovieDetail(BaseEndpoint):
    """Contains the page of one movie and the carousels shown on it.

    The carousels include "You Could Also Try", which `Carousel` reads by the
    token and the model given for it here.

    Source: https://pluto.tv/us/movies/{movie_id}/

    Example request:
        - POST /api/tn/hubs/graphql/
        - Host: pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Body: {"query": "query MovieHomeData(...) {...}", "variables": {...}}
    """

    # TODO: Validate
    def __call__(self, movie_id: str) -> MovieDetailModel:
        """Download and parse the movie detail file."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(movie_id), log_id)

    # TODO: Validate
    def download(self, movie_id: str) -> str:
        """Download the movie detail file.

        Raises:
            MovieNotFoundError: If the movie does not exist.
        """
        log_id = self.get_log_id(self.download, locals())
        response = self._client.download_graphql(QUERY, {"id": movie_id}, log_id)
        if extract_movie_detail(response) is None:
            raise MovieNotFoundError(movie_id, response)
        return response

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> MovieDetailModel:
        """Load a movie detail file into its model."""
        return model_validate_json(
            extract_movie_detail(data),
            log_id or self.default_log_id,
        )
