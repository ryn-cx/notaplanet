# TODO: Validate
"""Rebuilds CategoriesModel."""

from __future__ import annotations

import logging
from typing import Any

from get_around import build_client_automatically
from good_ass_pydantic_integrator import generate_model

from generate.constants import FILES_PATH, NOTAPLANET_PATH
from generate.utils import download_if_missing
from notaplanet import NotAPlanet

CATALOG_PAGES: dict[str, dict[str, Any]] = {
    "page_1": {"offset": 1},
    "page_1_no_items": {"offset": 1, "include_items": False},
    "page_999": {"page": 999, "offset": 1, "include_items": False},
}
"""The recorded pages of the catalog, and what each one was downloaded with."""


# TODO: Validate
def generate_categories(client: NotAPlanet) -> None:
    """Rebuild CategoriesModel."""
    for name, arguments in CATALOG_PAGES.items():
        download_if_missing(
            FILES_PATH,
            "CategoriesModel",
            name,
            lambda arguments=arguments: client.categories.download(**arguments),
        )
    generate_model(FILES_PATH, NOTAPLANET_PATH, "CategoriesModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_categories(NotAPlanet(build_client_automatically()))
