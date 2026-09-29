# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import SeasonsModel as OptionalModel
from .strict_models import SeasonsModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        Clip,
        Cover,
        Episode,
        FeaturedImage,
        Path,
        Poster169,
        Season,
        SeasonsModel,
        Stitched,
    )
else:
    from .optional_models import (
        Clip,
        Cover,
        Episode,
        FeaturedImage,
        Path,
        Poster169,
        Season,
        SeasonsModel,
        Stitched,
    )

__all__ = [
    "Clip",
    "Cover",
    "Episode",
    "FeaturedImage",
    "Path",
    "Poster169",
    "Season",
    "SeasonsModel",
    "Stitched",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> SeasonsModel:
    """Read a downloaded file into SeasonsModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
