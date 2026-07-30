# TODO: Validate
"""Contains the Items class."""

from __future__ import annotations

from http import HTTPStatus
from logging import NullHandler, getLogger
from typing import TYPE_CHECKING, Any, override

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.exceptions import ItemNotFoundError
from notaplanet.items.models import ItemsModel

if TYPE_CHECKING:
    from collections.abc import Sequence

    from good_ass_pydantic_integrator.constants import INPUT_TYPE

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Items(BaseEndpoint[ItemsModel]):
    """Manage the items file.

    Returns the metadata for one or more on-demand items. The accepted id is the
    `_id` of a series or of a movie, not the `seriesID` a movie is filed under
    and not the id of an individual episode.

    Source: https://pluto.tv/on-demand/series/{item_id}/details

    Example request:
        - GET /v4/vod/items?
            - ids={item_id}
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
        - TE: trailers
    """

    _response_model = ItemsModel

    @classmethod
    @override
    def transform_input(cls, data: INPUT_TYPE) -> INPUT_TYPE:
        """Wraps the top level JSON array so the model is a normal object model."""
        if isinstance(data, list):
            return {"items": data}
        return data

    @override
    def download(self, item_ids: Sequence[str]) -> list[dict[str, Any]]:
        log_id = self.get_log_id(self.download, locals())
        response = self._client.download(
            "vod",
            "v4/vod/items",
            params={"ids": ",".join(item_ids)},
            log_id=log_id,
        )
        return self._validate_download(response, list(item_ids))

    def _validate_download(
        self,
        response: list[dict[str, Any]],
        item_ids: list[str],
    ) -> list[dict[str, Any]]:
        # Unknown ids are dropped silently, so an empty list means every
        # requested id was unknown.
        if not response:
            raise ItemNotFoundError(item_ids, HTTPStatus.OK, response)
        return response

    @override
    def download_and_parse(self, item_ids: Sequence[str]) -> ItemsModel:
        return self.parse(self.download(item_ids))
