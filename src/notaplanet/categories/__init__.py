# TODO: Validate
"""Contains the Categories class."""

from __future__ import annotations

from collections.abc import Sequence
from logging import NullHandler, getLogger
from typing import TYPE_CHECKING, Any, override

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.categories.models import CategoriesModel
from notaplanet.exceptions import PageOutOfRangeError

if TYPE_CHECKING:
    from notaplanet.categories.models import Category

logger = getLogger(__name__)
logger.addHandler(NullHandler())

OFFSET = 20
"""Number of categories per page."""


class Categories(BaseEndpoint[CategoriesModel]):
    """Manage the categories file.

    Every on-demand category, optionally with the items that belong to it. This
    is the closest thing Pluto has to a full catalog listing.

    Source: https://pluto.tv/on-demand

    Example request:
        - GET /v4/vod/categories?
            - includeItems=true&
            - deviceType=web&
            - offset=20&
            - page=1
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

    _response_model = CategoriesModel

    @override
    def download(
        self,
        *,
        page: int = 1,
        offset: int = OFFSET,
        include_items: bool = True,
    ) -> dict[str, Any]:
        log_id = self.get_log_id(self.download, locals())
        response = self._client.download(
            "vod",
            "v4/vod/categories",
            params={
                "includeItems": str(include_items).lower(),
                "deviceType": "web",
                "offset": offset,
                "page": page,
            },
            log_id=log_id,
        )
        return self._validate_download(response, page)

    def _validate_download(
        self,
        response: dict[str, Any],
        page: int,
    ) -> dict[str, Any]:
        # A page past the last one comes back as a success with no categories
        # and without the totals that a real page carries.
        if not response.get("categories"):
            raise PageOutOfRangeError(page, response)
        return response

    def download_all_pages(
        self,
        *,
        offset: int = OFFSET,
        include_items: bool = True,
    ) -> list[dict[str, Any]]:
        """Downloads every page of categories."""
        results: list[dict[str, Any]] = []
        page = 1

        while True:
            response = self.download(
                page=page,
                offset=offset,
                include_items=include_items,
            )
            results.append(response)

            total_pages = response.get("totalPages")
            if total_pages is None or page >= total_pages:
                return results
            page += 1

    def parse_all_pages(self, datas: list[dict[str, Any]]) -> list[CategoriesModel]:
        """Parses the output of download_all_pages."""
        return [self.parse(data) for data in datas]

    @override
    def download_and_parse(
        self,
        *,
        page: int = 1,
        offset: int = OFFSET,
        include_items: bool = True,
    ) -> CategoriesModel:
        response = self.download(
            page=page,
            offset=offset,
            include_items=include_items,
        )
        return self.parse(response)

    def download_and_parse_all_pages(
        self,
        *,
        offset: int = OFFSET,
        include_items: bool = True,
    ) -> list[CategoriesModel]:
        """Downloads and parses every page of categories."""
        responses = self.download_all_pages(
            offset=offset,
            include_items=include_items,
        )
        return self.parse_all_pages(responses)

    def extract_categories(
        self,
        input_data: CategoriesModel
        | dict[str, Any]
        | Sequence[CategoriesModel | dict[str, Any]],
    ) -> list[Category]:
        """Extracts category entries from one or more files."""
        responses = input_data if isinstance(input_data, Sequence) else [input_data]

        result: list[Category] = []
        for response in responses:
            parsed = (
                response
                if isinstance(response, CategoriesModel)
                else self.parse(response)
            )
            result.extend(parsed.categories)
        return result
