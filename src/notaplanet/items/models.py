# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import ItemsModel as OptionalModel
from .strict_models import ItemsModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        Category,
        Clip,
        Cover,
        FeaturedImage,
        ItemsModel,
        ItemsModelItem,
        Path,
        Poster169,
        Stitched,
    )
else:
    from .optional_models import (
        Category,
        Clip,
        Cover,
        FeaturedImage,
        ItemsModel,
        ItemsModelItem,
        Path,
        Poster169,
        Stitched,
    )

__all__ = [
    "Category",
    "Clip",
    "Cover",
    "FeaturedImage",
    "ItemsModel",
    "ItemsModelItem",
    "Path",
    "Poster169",
    "Stitched",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> ItemsModel:
    """Read a downloaded file into ItemsModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
