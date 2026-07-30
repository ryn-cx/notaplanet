# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from notaplanet.exceptions import ItemNotFoundError
from tests.utils import assert_error, download_and_save, parsed_json

if TYPE_CHECKING:
    from notaplanet import NotAPlanet
    from notaplanet.items import Items

SERIES_ID = "60d0c64cd2de2a001300051d"
MOVIE_ID = "68f10fd8fa0f5ccff57520df"
INVALID_ITEM_ID = "000000000000000000000000"


@pytest.fixture(scope="session")
def client(client: NotAPlanet) -> Items:
    return client.items


def test_download(client: Items) -> None:
    download_and_save(client, SERIES_ID, lambda: client.download([SERIES_ID]))


def test_download_multiple(client: Items) -> None:
    download_and_save(
        client,
        f"{SERIES_ID}_{MOVIE_ID}",
        lambda: client.download([SERIES_ID, MOVIE_ID]),
    )


def test_parse(client: Items) -> None:
    data = parsed_json(client, SERIES_ID)
    assert [item.field_id for item in data.items] == [SERIES_ID]


def test_parse_multiple(client: Items) -> None:
    data = parsed_json(client, f"{SERIES_ID}_{MOVIE_ID}")
    assert sorted(item.field_id for item in data.items) == sorted(
        [SERIES_ID, MOVIE_ID],
    )


def test_download_invalid(client: Items) -> None:
    assert_error(
        client,
        INVALID_ITEM_ID,
        lambda: client.download([INVALID_ITEM_ID]),
        ItemNotFoundError,
    )
