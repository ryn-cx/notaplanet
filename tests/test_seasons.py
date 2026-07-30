# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from notaplanet.exceptions import PageOutOfRangeError, SeriesNotFoundError
from tests.utils import assert_error, download_and_save, parsed_json

if TYPE_CHECKING:
    from notaplanet import NotAPlanet
    from notaplanet.seasons import Seasons

SERIES_ID = "60d0c64cd2de2a001300051d"
INVALID_SERIES_ID = "000000000000000000000000"
OUT_OF_RANGE_PAGE = 99


@pytest.fixture(scope="session")
def client(client: NotAPlanet) -> Seasons:
    return client.seasons


def test_download(client: Seasons) -> None:
    download_and_save(client, SERIES_ID, lambda: client.download(SERIES_ID))


def test_parse(client: Seasons) -> None:
    data = parsed_json(client, SERIES_ID)
    assert data.field_id == SERIES_ID
    assert data.seasons


def test_download_invalid(client: Seasons) -> None:
    assert_error(
        client,
        INVALID_SERIES_ID,
        lambda: client.download(INVALID_SERIES_ID),
        SeriesNotFoundError,
    )


def test_download_invalid_page(client: Seasons) -> None:
    assert_error(
        client,
        f"{SERIES_ID}_page_{OUT_OF_RANGE_PAGE}",
        lambda: client.download(SERIES_ID, page=OUT_OF_RANGE_PAGE),
        PageOutOfRangeError,
    )
