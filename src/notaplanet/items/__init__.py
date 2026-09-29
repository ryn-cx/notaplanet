# TODO: Validate
"""Contains the Items class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import TYPE_CHECKING

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.items.models import ItemsModel, model_validate_json

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = getLogger(__name__)
logger.addHandler(NullHandler())


# TODO: Validate
class Items(BaseEndpoint):
    """Contains the items.

    The metadata for one or more on-demand titles. The accepted id is the `_id`
    of a series or of a movie, not the `seriesID` a movie is filed under and not
    the id of an individual episode. An id nothing is filed under is dropped from
    the answer instead of being refused.

    Source: https://pluto.tv/on-demand/series/{item_id}/details

    Example request:
        - GET /v4/vod/items?
            - ids={item_id}
        - Host: service-vod.clusters.pluto.tv
        - Origin: https://pluto.tv
        - Referer: https://pluto.tv/
        - Authorization: Bearer __REDACTED__
    """

    # TODO: Validate
    def __call__(self, item_ids: Sequence[str]) -> ItemsModel:
        """Download and parse the items file."""
        log_id = self.get_log_id(self.__call__, locals())
        return self.load(self.download(item_ids), log_id)

    # TODO: Validate
    def download(self, item_ids: Sequence[str]) -> str:
        """Download the items file."""
        log_id = self.get_log_id(self.download, locals())
        return self._client.download(
            "vod",
            "v4/vod/items",
            {"ids": ",".join(item_ids)},
            log_id,
        )

    # TODO: Validate
    def load(self, data: str, log_id: str = "") -> ItemsModel:
        """Load a items file into its model."""
        return model_validate_json(data, log_id or self.default_log_id)
