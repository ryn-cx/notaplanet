from __future__ import annotations

import logging
from typing import Any

from get_around import build_client_automatically
from good_ass_pydantic_integrator.recordings import (
    RecordingId,
    download_missing,
    load_ids,
    rebuild_model,
)
from pydantic import model_validator

from generate.constants import GENERATOR_PATHS
from notaplanet import NotAPlanet

MODEL_NAME = "ItemsModel"


# TODO: Validate
class ItemsId(RecordingId[NotAPlanet]):
    item_ids: list[str]

    # TODO: Validate
    @model_validator(mode="before")
    @classmethod
    def read_entry(cls, entry: Any) -> Any:  # noqa: ANN401
        if isinstance(entry, list):
            return {"item_ids": entry}
        return entry

    # TODO: Validate
    def recording_name(self) -> str:
        return "_".join(self.item_ids)

    # TODO: Validate
    def download(self, client: NotAPlanet) -> str:
        return client.items.download(self.item_ids)


ITEM_ID_SETS = load_ids(GENERATOR_PATHS, MODEL_NAME, ItemsId)


# TODO: Validate
def generate_items(client: NotAPlanet) -> None:
    download_missing(GENERATOR_PATHS, MODEL_NAME, ITEM_ID_SETS, client)
    rebuild_model(GENERATOR_PATHS, MODEL_NAME, ItemsId)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    generate_items(NotAPlanet(build_client_automatically()))
