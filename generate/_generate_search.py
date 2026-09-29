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

MODEL_NAME = "SearchModel"


# TODO: Validate
class SearchId(RecordingId[NotAPlanet]):
    query: str

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.search.download(self.query)


QUERIES = load_ids(GENERATOR_PATHS, MODEL_NAME, SearchId)


# TODO: Validate
def generate_search(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, QUERIES, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, SearchId)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_search(NotAPlanet(build_client_automatically()))
