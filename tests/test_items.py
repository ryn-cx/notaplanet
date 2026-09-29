# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Sequence

    from notaplanet import NotAPlanet

SERIES_ID = "56dde345efda194e6684a5b5"
"""The series Gun, which has one season."""

MOVIE_ID = "5c9c08adc8ccd6797db67cd8"
"""The movie The Shootist."""

UNKNOWN_ID = "000000000000000000000000"
"""An id nothing is filed under."""

ITEM_ID_SETS = [
    pytest.param((SERIES_ID,), id="series"),
    pytest.param((SERIES_ID, MOVIE_ID), id="series and movie"),
    pytest.param((UNKNOWN_ID,), id="item that does not exist"),
]


# TODO: Validate
@pytest.mark.parametrize("item_ids", ITEM_ID_SETS)
def test_download(client: NotAPlanet, item_ids: Sequence[str]) -> None:
    items = client.items(item_ids)
    # An id nothing is filed under is dropped from the answer instead of being
    # refused, so asking only for unknown ids gives an empty array.
    known_ids = [item_id for item_id in item_ids if item_id != UNKNOWN_ID]
    assert [item.field_id for item in items.root] == known_ids
