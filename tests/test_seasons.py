# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from notaplanet import NotAPlanet

SERIES_ID = "56dde345efda194e6684a5b5"
"""The series Gun, which has one season."""

PAGES = [
    pytest.param(1, 1, id="every season of gun"),
    pytest.param(99, 0, id="page past the last one"),
]


# TODO: Validate
@pytest.mark.parametrize(("page", "season_count"), PAGES)
def test_download(client: NotAPlanet, page: int, season_count: int) -> None:
    seasons = client.seasons(SERIES_ID, page=page)
    assert seasons.field_id == SERIES_ID
    # A page past the last one is answered with the series and no seasons.
    assert len(seasons.seasons) == season_count
