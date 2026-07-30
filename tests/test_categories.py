# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from notaplanet.categories import OFFSET
from notaplanet.exceptions import PageOutOfRangeError
from tests.utils import assert_error, download_and_save, loaded_json, parsed_json

if TYPE_CHECKING:
    from notaplanet import NotAPlanet
    from notaplanet.categories import Categories

OUT_OF_RANGE_PAGE = 999


@pytest.fixture(scope="session")
def client(client: NotAPlanet) -> Categories:
    return client.categories


def test_download(client: Categories) -> None:
    download_and_save(client, 1, lambda: client.download(page=1))


def test_download_all_pages(client: Categories) -> None:
    download_and_save(
        client,
        "all_pages",
        client.download_all_pages,
        "Multipage",
    )


def test_download_invalid_page(client: Categories) -> None:
    assert_error(
        client,
        OUT_OF_RANGE_PAGE,
        lambda: client.download(page=OUT_OF_RANGE_PAGE),
        PageOutOfRangeError,
    )


def test_parse(client: Categories) -> None:
    data = parsed_json(client, 1)
    assert len(data.categories) == OFFSET


def test_parse_all_pages(client: Categories) -> None:
    results = parsed_json(client, "all_pages", category="Multipage")
    assert len(results) > 1
    for result in results:
        assert result.categories


def test_extract_categories(client: Categories) -> None:
    loaded = loaded_json(client, 1)
    extracted_loaded = client.extract_categories(loaded)

    data = parsed_json(client, 1)
    extracted_data = client.extract_categories(data)
    assert extracted_data == extracted_loaded
    assert len(extracted_data) == OFFSET


def test_extract_categories_all_pages(client: Categories) -> None:
    loaded = loaded_json(client, "all_pages", category="Multipage")
    extracted_loaded = client.extract_categories(loaded)

    data = parsed_json(client, "all_pages", category="Multipage")
    extracted_data = client.extract_categories(data)
    assert extracted_data == extracted_loaded
    assert len(extracted_data) > OFFSET
