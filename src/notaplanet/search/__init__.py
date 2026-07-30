# TODO: Validate
"""Contains the Search class."""

from __future__ import annotations

from logging import NullHandler, getLogger
from typing import Any, override

from notaplanet.base_api_endpoint import BaseEndpoint
from notaplanet.search.models import SearchModel

logger = getLogger(__name__)
logger.addHandler(NullHandler())

LIMIT = 10


class Search(BaseEndpoint[SearchModel]):
    """Manage the search file.

    Search never reports zero results. A query that matches nothing is padded
    out with loosely related titles, so there is no error case to detect.

    Source: https://pluto.tv/search?query={query}

    Example request:
        - GET /v1/search?
            - q={query}&
            - limit=10&
            - includeItems=true&
            - deviceType=web
            - HTTP/2
        - Host: service-media-search.clusters.pluto.tv
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

    _response_model = SearchModel

    @override
    def download(
        self,
        q: str,
        *,
        limit: int = LIMIT,
        include_items: bool = True,
    ) -> dict[str, Any]:
        log_id = self.get_log_id(self.download, locals())
        return self._client.download(
            "search",
            "v1/search",
            params={
                "q": q,
                "limit": limit,
                "includeItems": str(include_items).lower(),
                "deviceType": "web",
            },
            log_id=log_id,
        )

    @override
    def download_and_parse(
        self,
        q: str,
        *,
        limit: int = LIMIT,
        include_items: bool = True,
    ) -> SearchModel:
        return self.parse(self.download(q, limit=limit, include_items=include_items))
