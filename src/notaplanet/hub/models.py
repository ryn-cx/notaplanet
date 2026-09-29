# ruff: noqa: D100
from typing import TYPE_CHECKING

from good_ass_pydantic_integrator import load

from .optional_models import HubModel as OptionalModel
from .strict_models import HubModel as StrictModel

if TYPE_CHECKING:
    from .strict_models import (
        HubCarousel,
        HubModel,
    )
else:
    from .optional_models import (
        HubCarousel,
        HubModel,
    )

__all__ = [
    "HubCarousel",
    "HubModel",
    "model_validate_json",
]


def model_validate_json(data: str | bytes | object, log_id: str) -> HubModel:
    """Read a downloaded file into HubModel."""
    return load.model_validate_json(StrictModel, OptionalModel, data, log_id)
