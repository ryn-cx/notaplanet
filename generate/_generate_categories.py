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

MODEL_NAME = "CategoriesModel"


# TODO: Validate
class CategoriesId(RecordingId[NotAPlanet]):
    written_as_fields = True

    offset: int
    include_items: bool | None = None
    page: int | None = None

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.categories.download(**self.model_dump(exclude_unset=True))


CATALOG_PAGES = load_ids(GENERATOR_PATHS, MODEL_NAME, CategoriesId)


# TODO: Validate
def generate_categories(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, CATALOG_PAGES, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, CategoriesId)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_categories(NotAPlanet(build_client_automatically()))
