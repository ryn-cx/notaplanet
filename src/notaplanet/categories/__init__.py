# TODO: Validate
"""Contains the Categories class."""

from __future__ import annotations

from logging import NullHandler, getLogger

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.categories.models import CategoriesModel, model_validate_json

logger = getLogger(__name__)
logger.addHandler(NullHandler())

OFFSET = 20
"""Number of titles listed per category."""


# TODO: Validate
class Categories(BaseEndpoint):
    """Manage the categories file.

    One page of the on-demand catalog, which is the closest thing Pluto has to a
    full listing.

    Source: https://pluto.tv/on-demand

    Example request:
        - GET /v4/vod/categories?
            - includeItems=true&
            - deviceType=web&
            - offset=20&
            - page=1
        - Host: service-vod.clusters.pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Authorization: Bearer __REDACTED__
    """

    # TODO: Validate
    def __call__(
        self,
        *,
        page: int = 1,
        offset: int = OFFSET,
        include_items: bool = True,
    ) -> CategoriesModel:
        """Look the categories up and return the model they are read into."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(
            self.download(page=page, offset=offset, include_items=include_items),
            log_id,
        )

    # TODO: Validate
    def download(
        self,
        *,
        page: int = 1,
        offset: int = OFFSET,
        include_items: bool = True,
    ) -> str:
        """Download the categories file."""
        log_id = self.get_log_id(self.download, locals())
        return self._client.download(
            "vod",
            "v4/vod/categories",
            {
                "includeItems": str(include_items).lower(),
                "deviceType": "web",
                "offset": offset,
                "page": page,
            },
            log_id,
        )

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> CategoriesModel:
        """Read a downloaded categories file into its model."""
        return model_validate_json(data, log_id or self.default_log_id)
