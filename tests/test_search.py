# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from notaplanet import NotAPlanet

QUERIES = [
    pytest.param("Gunsmoke", id="query that matches titles"),
    pytest.param("zzzqqqxxnotathing", id="query that matches nothing"),
]


# TODO: Validate
@pytest.mark.parametrize("query", QUERIES)
def test_download(client: NotAPlanet, query: str) -> None:
    # A query that matches nothing is padded out with loosely related titles, so
    # every query has results.
    assert client.search(query).data
