# TODO: Validate
"""Contains the Search class."""

from __future__ import annotations

from logging import NullHandler, getLogger

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.search.models import SearchModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

LIMIT = 10
"""Number of results the web player asks for."""


# TODO: Validate
class Search(BaseEndpoint):
    """Manage the search file.

    A query that matches nothing is padded out with loosely related titles, so
    search never answers with no results.

    Source: https://pluto.tv/search?query={query}

    Example request:
        - GET /v1/search?
            - q={query}&
            - limit=10&
            - includeItems=true&
            - deviceType=web
        - Host: service-media-search.clusters.pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Authorization: Bearer __REDACTED__
    """

    # TODO: Validate
    def __call__(
        self,
        q: str,
        *,
        limit: int = LIMIT,
        include_items: bool = True,
    ) -> SearchModel:
        """Run the search and return the model it is read into."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(
            self.download(q, limit=limit, include_items=include_items),
            log_id,
        )

    # TODO: Validate
    def download(
        self,
        q: str,
        *,
        limit: int = LIMIT,
        include_items: bool = True,
    ) -> str:
        """Download the search file."""
        log_id = self.get_log_id(self.download, locals())
        return self._client.download(
            "search",
            "v1/search",
            {
                "q": q,
                "limit": limit,
                "includeItems": str(include_items).lower(),
                "deviceType": "web",
            },
            log_id,
        )

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> SearchModel:
        """Read a downloaded search file into its model."""
        return model_validate_json(data, log_id or type(self).__name__)
