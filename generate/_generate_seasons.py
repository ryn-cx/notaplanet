from __future__ import annotations

import logging

from get_around import build_client_automatically
from good_ass_pydantic_integrator.recordings import (
    RecordingId,
    download_named_missing,
    load_named_ids,
    rebuild_model,
)

from generate.constants import GENERATOR_PATHS
from notaplanet import NotAPlanet

MODEL_NAME = "SeasonsModel"


# TODO: Validate
class SeasonsId(RecordingId[NotAPlanet]):
    written_as_fields = True

    series_id: str
    page: int

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.seasons.download(**self.model_dump(exclude_unset=True))


SEASONS_REQUESTS = load_named_ids(GENERATOR_PATHS, MODEL_NAME, SeasonsId)


# TODO: Validate
def generate_seasons(client: NotAPlanet) -> None:
    download_named_missing(GENERATOR_PATHS, MODEL_NAME, SEASONS_REQUESTS, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, SeasonsId)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_seasons(NotAPlanet(build_client_automatically()))
