# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from notaplanet.search.models import SearchModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from notaplanet import NotAPlanet

QUERIES = [
    pytest.param("Gunsmoke", id="query that matches titles"),
    pytest.param("zzzqqqxxnotathing", id="query that matches nothing"),
]


class SearchTest(RecordedEndpoint):
    MODEL = SearchModel
    # Which titles a query matches and what the search box would offer to
    # finish it with are re-ranked as the catalog changes.
    IGNORED = ("SearchModel.data", "SearchModel.trending", "Suggestions.autocomplete")


# TODO: Validate
@pytest.mark.parametrize("query", QUERIES)
def test_download(client: NotAPlanet, query: str) -> None:
    SearchTest.download_test(query, lambda: client.search.download(query))


# TODO: Validate
@pytest.mark.parametrize("query", QUERIES)
def test_parse(client: NotAPlanet, query: str) -> None:
    results = client.search.load(SearchTest.recorded_content(query))
    # A query that matches nothing is padded out with loosely related titles, so
    # every query has results.
    assert results.data
