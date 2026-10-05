# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import MovieDetailModel as OptionalModel
from .strict_models import MovieDetailModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        CarouselConfig,
        Movie,
        MovieAssets,
        MovieDetailModel,
        RegionalRating,
    )
else:
    from .optional_models import (
        CarouselConfig,
        Movie,
        MovieAssets,
        MovieDetailModel,
        RegionalRating,
    )

__all__ = [
    "CarouselConfig",
    "Movie",
    "MovieAssets",
    "MovieDetailModel",
    "RegionalRating",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> MovieDetailModel:
    """Read a downloaded file into MovieDetailModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
