# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from notaplanet.exceptions import SeriesNotFoundError
from notaplanet.seasons.models import SeasonsModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from notaplanet import NotAPlanet

SERIES_ID = "56dde345efda194e6684a5b5"
"""The series Gun, which has one season."""

SEASONS_PAGES = [
    pytest.param(SERIES_ID, {}, id="every season of gun"),
    pytest.param(f"{SERIES_ID}_page_99", {"page": 99}, id="page past the last one"),
]

RECORDED_SEASON_COUNTS = [
    pytest.param(SERIES_ID, 1, id="every season of gun"),
    pytest.param(f"{SERIES_ID}_page_99", 0, id="page past the last one"),
]


class SeasonsTest(RecordedEndpoint):
    MODEL = SeasonsModel


# TODO: Validate
@pytest.mark.parametrize(("name", "arguments"), SEASONS_PAGES)
def test_download(client: NotAPlanet, name: str, arguments: dict[str, Any]) -> None:
    SeasonsTest.download_test(
        name,
        lambda: client.seasons.download(SERIES_ID, **arguments),
    )


# TODO: Validate
@pytest.mark.parametrize(("name", "season_count"), RECORDED_SEASON_COUNTS)
def test_parse(client: NotAPlanet, name: str, season_count: int) -> None:
    seasons = client.seasons.load(SeasonsTest.recorded_content(name))
    assert seasons.field_id == SERIES_ID
    # A page past the last one is answered with the series and no seasons.
    assert len(seasons.seasons) == season_count


# TODO: Validate
@pytest.mark.parametrize(
    "series_id",
    [
        pytest.param("000000000000000000000000", id="series that does not exist"),
        pytest.param("nonsense", id="series id that is not shaped like one"),
    ],
)
def test_download_invalid(client: NotAPlanet, series_id: str) -> None:
    SeasonsTest.error_test(
        series_id,
        lambda: client.seasons.download(series_id),
        SeriesNotFoundError,
    )
