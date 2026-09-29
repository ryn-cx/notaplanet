# TODO: Validate
"""Contains the Hub class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger
from typing import Any

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.exceptions import GraphQLError, HubNotFoundError
from notaplanet.hub.models import HubModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

QUERY = """
query CollectionApiResponse(
    $slug: String,
    $isChildCategory: Boolean,
    $extraParams: JSON
) {
    collection(
        slug: $slug,
        isChildCategory: $isChildCategory,
        extraParams: $extraParams
    ) {
        success
        hubId
        title
        hubSlug
        type
        heroToken
        marqueeToken
        hubCarousels {
            position
            token
            carouselPresentationStyle
            carouselId
            isContentHighlightEnabled
            title
            model
            displayTitle
            href
            carouselType
        }
        pageType
        region
        locale
        userState
        liveOnDate
        start
        rows
        total
    }
}
"""


# TODO: Validate
def extract_hub(response: str) -> dict[str, Any]:
    """Extract the hub from the GraphQL response."""
    return json.loads(response)["data"]["collection"]


# TODO: Validate
class Hub(BaseEndpoint):
    """Contains one hub of the website, such as Comedy Shows or All Movies.

    The titles are in the carousels, which `Carousel` reads by the token the hub
    carries for each one.

    Source: https://pluto.tv/us/shows/category/{category}/

    Example request:
        - POST /api/tn/hubs/graphql/
        - Host: pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Body: {"query": "query CollectionApiResponse(...) {...}", "variables": {...}}
    """

    # TODO: Validate
    def __call__(self, hub_slug: str) -> HubModel:
        """Download and parse the hub file."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(hub_slug), log_id)

    # TODO: Validate
    def download(self, hub_slug: str) -> str:
        """Download the hub file.

        Raises:
            HubNotFoundError: If the hub does not exist.
        """
        log_id = self.get_log_id(self.download, locals())
        try:
            return self._client.download_graphql(
                QUERY,
                {"slug": hub_slug, "isChildCategory": False, "extraParams": {}},
                log_id,
            )
        except GraphQLError as err:
            if "API_DATA_ERROR" in err.codes:
                raise HubNotFoundError(hub_slug, err.response) from err
            raise

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> HubModel:
        """Load a hub file into its model."""
        return model_validate_json(extract_hub(data), log_id or self.default_log_id)
