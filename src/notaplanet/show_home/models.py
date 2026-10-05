# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import ShowHomeModel as OptionalModel
from .strict_models import ShowHomeModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        CarouselConfig,
        RegionalRating,
        Season,
        Show,
        ShowAssets,
        ShowHomeModel,
    )
else:
    from .optional_models import (
        CarouselConfig,
        RegionalRating,
        Season,
        Show,
        ShowAssets,
        ShowHomeModel,
    )

__all__ = [
    "CarouselConfig",
    "RegionalRating",
    "Season",
    "Show",
    "ShowAssets",
    "ShowHomeModel",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> ShowHomeModel:
    """Read a downloaded file into ShowHomeModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
