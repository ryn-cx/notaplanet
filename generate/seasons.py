# TODO: Validate
"""Rebuilds SeasonsModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NOTAPLANET_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from notaplanet import NotAPlanet

SEASONS_REQUESTS = load_ids("SeasonsModel")
"""What each recording of a seasons response was downloaded with."""


# TODO: Validate
def generate_seasons(client: NotAPlanet) -> None:
    """Rebuild SeasonsModel."""
    for name, arguments in SEASONS_REQUESTS.items():
        download_if_missing(
            FILES_PATH,
            "SeasonsModel",
            name,
            lambda arguments=arguments: client.seasons.download(**arguments),
        )
    rebuild_model(FILES_PATH, NOTAPLANET_PATH, "SeasonsModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_seasons(NotAPlanet(build_client_automatically()))
