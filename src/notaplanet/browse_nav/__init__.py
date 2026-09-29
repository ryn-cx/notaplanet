# TODO: Validate
"""Contains the BrowseNav class."""

from __future__ import annotations

import json
from logging import NullHandler, getLogger
from typing import Any

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.browse_nav.models import BrowseNavModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

QUERY = """
query browseNav($extraParams: UserParams!) {
    browseNav(version: "v2.1", extraParams: $extraParams) {
        globalMenu {
            showBrowseNav {
                id
                label
                slug
                type
                href
                locale
            }
            movieBrowseNav {
                id
                label
                slug
                type
                href
                locale
            }
        }
    }
}
"""


# TODO: Validate
def extract_browse_nav(response: str) -> dict[str, Any]:
    """Extract the browse nav from the GraphQL response."""
    return json.loads(response)["data"]["browseNav"]


# TODO: Validate
class BrowseNav(BaseEndpoint):
    """Contains the hubs listed in the Shows and Movies menus of the website.

    Each hub is read by its slug with `Hub`.

    Source: https://pluto.tv/us/shows/category/all-shows/

    Example request:
        - POST /api/tn/hubs/graphql/
        - Host: pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Body: {"query": "query browseNav(...) {...}", "variables": {...}}
    """

    # TODO: Validate
    def __call__(self) -> BrowseNavModel:
        """Download and parse the browse nav file."""
        return self.load(self.download(), self.default_log_id)

    # TODO: Validate
    def download(self) -> str:
        """Download the browse nav file."""
        return self._client.download_graphql(
            QUERY,
            {"extraParams": {}},
            self.default_log_id,
        )

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> BrowseNavModel:
        """Load a browse nav file into its model."""
        return model_validate_json(
            extract_browse_nav(data),
            log_id or self.default_log_id,
        )
