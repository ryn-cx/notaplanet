# TODO: Validate
"""Rebuilds ItemsModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NOTAPLANET_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from notaplanet import NotAPlanet

SERIES_ID = "56dde345efda194e6684a5b5"
"""The series Gun, which has one season."""

MOVIE_ID = "5c9c08adc8ccd6797db67cd8"
"""The movie The Shootist."""

UNKNOWN_ID = "000000000000000000000000"
"""An id nothing is filed under."""

ITEM_ID_SETS = load_ids("ItemsModel")
"""The sets of ids the recorded item files were downloaded for."""


# TODO: Validate
def generate_items(client: NotAPlanet) -> None:
    """Rebuild ItemsModel."""
    for item_ids in ITEM_ID_SETS:
        download_if_missing(
            FILES_PATH,
            "ItemsModel",
            "_".join(item_ids),
            lambda item_ids=item_ids: client.items.download(item_ids),
        )
    rebuild_model(
        FILES_PATH,
        NOTAPLANET_PATH,
        "ItemsModel",
        name_of="_".join,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_items(NotAPlanet(build_client_automatically()))
