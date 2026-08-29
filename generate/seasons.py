# TODO: Validate
"""Rebuilds SeasonsModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NOTAPLANET_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from notaplanet import NotAPlanet

SERIES_ID = "56dde345efda194e6684a5b5"
"""The series Gun, which has one season."""

SEASONS_PAGES = load_ids("SeasonsModel")
"""The recorded seasons files, and the page of the series each one holds."""


# TODO: Validate
def generate_seasons(client: NotAPlanet) -> None:
    """Rebuild SeasonsModel."""
    for name, page in SEASONS_PAGES.items():
        download_if_missing(
            FILES_PATH,
            "SeasonsModel",
            name,
            lambda page=page: client.seasons.download(SERIES_ID, page=page),
        )
    rebuild_model(FILES_PATH, NOTAPLANET_PATH, "SeasonsModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_seasons(NotAPlanet(build_client_automatically()))
