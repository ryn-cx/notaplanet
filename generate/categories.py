# TODO: Validate
"""Rebuilds CategoriesModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NOTAPLANET_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from notaplanet import NotAPlanet

CATALOG_PAGES = load_ids("CategoriesModel")
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
    rebuild_model(FILES_PATH, NOTAPLANET_PATH, "CategoriesModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_categories(NotAPlanet(build_client_automatically()))
