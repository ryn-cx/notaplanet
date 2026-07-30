# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utils import download_and_save, parsed_json

if TYPE_CHECKING:
    from notaplanet import NotAPlanet
    from notaplanet.search import Search

QUERY = "Gunsmoke"
UNMATCHED_QUERY = "zzzqqqxxnotathing"


@pytest.fixture(scope="session")
def client(client: NotAPlanet) -> Search:
    return client.search


def test_download(client: Search) -> None:
    download_and_save(client, QUERY, lambda: client.download(QUERY))


def test_download_unmatched(client: Search) -> None:
    download_and_save(
        client,
        UNMATCHED_QUERY,
        lambda: client.download(UNMATCHED_QUERY),
    )


def test_parse(client: Search) -> None:
    data = parsed_json(client, QUERY)
    assert QUERY in [item.name for item in data.data]


def test_parse_unmatched(client: Search) -> None:
    # Search never reports zero results. A query that matches nothing is padded
    # out with loosely related titles instead, so the only thing worth asserting
    # is that none of them are the query.
    data = parsed_json(client, UNMATCHED_QUERY)
    assert data.data
    assert UNMATCHED_QUERY not in [item.name for item in data.data]
