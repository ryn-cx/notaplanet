# TODO: Validate
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
from notaplanet.show_home import extract_show_home

MODEL_NAME = "ShowHomeModel"


# TODO: Validate
class ShowHomeId(RecordingId[NotAPlanet]):
    slug: str

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.show_home.download(self.slug)


SLUGS = load_ids(GENERATOR_PATHS, MODEL_NAME, ShowHomeId)


# TODO: Validate
def generate_show_home(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, SLUGS, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, ShowHomeId, extract_show_home)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_show_home(NotAPlanet(build_client_automatically()))
