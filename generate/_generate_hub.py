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
from notaplanet.hub import extract_hub

MODEL_NAME = "HubModel"


# TODO: Validate
class HubId(RecordingId[NotAPlanet]):
    hub_slug: str

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.hub.download(self.hub_slug)


HUB_SLUGS = load_ids(GENERATOR_PATHS, MODEL_NAME, HubId)


# TODO: Validate
def generate_hub(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, HUB_SLUGS, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, HubId, extract_hub)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_hub(NotAPlanet(build_client_automatically()))
