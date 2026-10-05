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
from notaplanet.movie_detail import extract_movie_detail

MODEL_NAME = "MovieDetailModel"


# TODO: Validate
class MovieDetailId(RecordingId[NotAPlanet]):
    movie_id: str

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.movie_detail.download(self.movie_id)


MOVIE_IDS = load_ids(GENERATOR_PATHS, MODEL_NAME, MovieDetailId)


# TODO: Validate
def generate_movie_detail(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, MOVIE_IDS, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, MovieDetailId, extract_movie_detail)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_movie_detail(NotAPlanet(build_client_automatically()))
