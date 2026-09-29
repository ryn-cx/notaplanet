# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import BrowseNavModel as OptionalModel
from .strict_models import BrowseNavModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        BrowseNavModel,
        GlobalMenu,
        MovieBrowseNavItem,
        ShowBrowseNavItem,
    )
else:
    from .optional_models import (
        BrowseNavModel,
        GlobalMenu,
        MovieBrowseNavItem,
        ShowBrowseNavItem,
    )

__all__ = [
    "BrowseNavModel",
    "GlobalMenu",
    "MovieBrowseNavItem",
    "ShowBrowseNavItem",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> BrowseNavModel:
    """Read a downloaded file into BrowseNavModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
