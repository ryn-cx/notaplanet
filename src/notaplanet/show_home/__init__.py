# TODO: Validate
"""Contains the ShowHome class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger
from typing import Any

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.exceptions import ShowNotFoundError
from notaplanet.show_home.models import ShowHomeModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

QUERY = """
query ShowHomeData($slug: String!) {
    showHome(slug: $slug) {
        show {
            id
            slug
            title
            showAssets {
                filepath_video_endcard_show_image
            }
            logo
            callout
            premiereDate
            description
            shortDescription
            longDescription
            genre
            category
            brand
            brandUrl
            numSeasons
            showEpisodeGuideLink
            isLocked
            showEpisodeTitle
            showEpisodeId
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
        }
    }
}
"""


# TODO: Validate
def extract_show_home(response: str) -> dict[str, Any] | None:
    """Extract the show home from the GraphQL response."""
    return json.loads(response)["data"]["showHome"]


# TODO: Validate
class ShowHome(BaseEndpoint):
    """Contains the page of one show and the carousels shown on it.

    The carousels include "You Could Also Try", which `Carousel` reads by the
    token and the model given for it here.

    Source: https://pluto.tv/us/shows/{slug}/

    Example request:
        - POST /api/tn/hubs/graphql/
        - Host: pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Body: {"query": "query ShowHomeData(...) {...}", "variables": {...}}
    """

    # TODO: Validate
    def __call__(self, slug: str) -> ShowHomeModel:
        """Download and parse the show home file."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(slug), log_id)

    # TODO: Validate
    def download(self, slug: str) -> str:
        """Download the show home file.

        Raises:
            ShowNotFoundError: If the show does not exist.
        """
        log_id = self.get_log_id(self.download, locals())
        response = self._client.download_graphql(QUERY, {"slug": slug}, log_id)
        if extract_show_home(response) is None:
            raise ShowNotFoundError(slug, response)
        return response

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> ShowHomeModel:
        """Load a show home file into its model."""
        return model_validate_json(
            extract_show_home(data),
            log_id or self.default_log_id,
        )
