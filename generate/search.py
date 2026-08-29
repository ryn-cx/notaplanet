# TODO: Validate
"""Rebuilds SearchModel."""

from __future__ import annotations

import logging

from get_around import build_client_automatically

from generate.constants import FILES_PATH, NOTAPLANET_PATH
from generate.utils import download_if_missing, load_ids, rebuild_model
from notaplanet import NotAPlanet

QUERIES = load_ids("SearchModel")
"""A query that matches titles, and one that matches nothing."""


# TODO: Validate
def generate_search(client: NotAPlanet) -> None:
    """Rebuild SearchModel."""
    for query in QUERIES:
        download_if_missing(
            FILES_PATH,
            "SearchModel",
            query,
            lambda query=query: client.search.download(query),
        )
    rebuild_model(FILES_PATH, NOTAPLANET_PATH, "SearchModel")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_search(NotAPlanet(build_client_automatically()))
