# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from notaplanet import NotAPlanet

PAGES = [
    pytest.param(1, id="first page"),
    pytest.param(999, id="page past the last one"),
]


# TODO: Validate
@pytest.mark.parametrize("page", PAGES)
def test_download(client: NotAPlanet, page: int) -> None:
    assert client.categories(page=page, offset=1).page == page


# TODO: Validate
def test_download_without_items(client: NotAPlanet) -> None:
    # A category is listed without the titles under it when they are not asked for.
    categories = client.categories(offset=1, include_items=False)
    assert all(not category.items for category in categories.categories)
