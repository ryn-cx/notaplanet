# TODO: Validate
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from notaplanet.categories.models import CategoriesModel
from tests.utils import RecordedEndpoint

if TYPE_CHECKING:
    from notaplanet import NotAPlanet

CATEGORY_PAGES = [
    pytest.param("page_1", {"offset": 1}, id="first page with titles"),
    pytest.param(
        "page_1_no_items",
        {"offset": 1, "include_items": False},
        id="first page without titles",
    ),
    pytest.param(
        "page_999",
        {"page": 999, "offset": 1, "include_items": False},
        id="page past the last one",
    ),
]

RECORDED_PAGE_NUMBERS = [
    pytest.param("page_1", 1, id="first page with titles"),
    pytest.param("page_1_no_items", 1, id="first page without titles"),
    pytest.param("page_999", 999, id="page past the last one"),
]


class CategoriesTest(RecordedEndpoint):
    MODEL = CategoriesModel
    # The catalog is re-ranked and resized as titles come and go, so the totals
    # and the titles listed under a category move on their own.
    IGNORED = (
        "CategoriesModel.total_categories",
        "CategoriesModel.total_pages",
        "Category.total_items_count",
        "Category.items",
    )


# TODO: Validate
@pytest.mark.parametrize(("name", "arguments"), CATEGORY_PAGES)
def test_download(client: NotAPlanet, name: str, arguments: dict[str, Any]) -> None:
    CategoriesTest.download_test(
        name,
        lambda: client.categories.download(**arguments),
    )


# TODO: Validate
@pytest.mark.parametrize(("name", "page"), RECORDED_PAGE_NUMBERS)
def test_parse(client: NotAPlanet, name: str, page: int) -> None:
    categories = client.categories.load(CategoriesTest.recorded_content(name))
    assert categories.page == page
