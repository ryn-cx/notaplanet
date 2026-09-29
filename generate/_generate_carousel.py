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
from notaplanet.carousel import extract_carousel

MODEL_NAME = "CarouselModel"


# TODO: Validate
class CarouselId(RecordingId[NotAPlanet]):
    hub_slug: str
    carousel_id: str

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        carousel = next(
            carousel
            for carousel in client.hub(self.hub_slug).hub_carousels
            if carousel.carousel_id == self.carousel_id
        )
        return client.carousel.download(carousel.token, model=carousel.model)


CAROUSELS = load_ids(GENERATOR_PATHS, MODEL_NAME, CarouselId)


# TODO: Validate
def generate_carousel(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, CAROUSELS, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, CarouselId, extract_carousel)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_carousel(NotAPlanet(build_client_automatically()))
