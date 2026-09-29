# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import SearchModel as OptionalModel
from .strict_models import SearchModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        AutocompleteItem,
        Datum,
        DistributeAs,
        Image,
        SearchModel,
        Suggestions,
        TrendingItem,
    )
else:
    from .optional_models import (
        AutocompleteItem,
        Datum,
        DistributeAs,
        Image,
        SearchModel,
        Suggestions,
        TrendingItem,
    )

__all__ = [
    "AutocompleteItem",
    "Datum",
    "DistributeAs",
    "Image",
    "SearchModel",
    "Suggestions",
    "TrendingItem",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> SearchModel:
    """Read a downloaded file into SearchModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
