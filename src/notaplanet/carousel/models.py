# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import CarouselModel as OptionalModel
from .strict_models import CarouselModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        CarouselModel,
        Datum,
        Result,
    )
else:
    from .optional_models import (
        CarouselModel,
        Datum,
        Result,
    )

__all__ = [
    "CarouselModel",
    "Datum",
    "Result",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> CarouselModel:
    """Read a downloaded file into CarouselModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
