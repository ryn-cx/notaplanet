from __future__ import annotations

import logging

from get_around import build_client_automatically
from good_ass_pydantic_integrator.recordings import (
    RecordingId,
    download_missing,
    load_ids,
    rebuild_model,
)

from generate.constants import GENERATOR_PATHS
from notaplanet import NotAPlanet
from notaplanet.browse_nav import extract_browse_nav

MODEL_NAME = "BrowseNavModel"


# TODO: Validate
class BrowseNavId(RecordingId[NotAPlanet]):
    name: str

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.browse_nav.download()


NAMES = load_ids(GENERATOR_PATHS, MODEL_NAME, BrowseNavId)


# TODO: Validate
def generate_browse_nav(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, NAMES, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, BrowseNavId, extract_browse_nav)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_browse_nav(NotAPlanet(build_client_automatically()))
