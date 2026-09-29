from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from pydantic import BaseModel, Field

class ShowBrowseNavItem(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    label: str
    slug: str
    type: str
    href: str
    locale: str

class MovieBrowseNavItem(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    label: str
    slug: str
    type: str
    href: str
    locale: str

class GlobalMenu(BaseModel):
    model_config = ConfigDict(defer_build=True)
    show_browse_nav: list[ShowBrowseNavItem] = Field(..., alias='showBrowseNav')
    movie_browse_nav: list[MovieBrowseNavItem] = Field(..., alias='movieBrowseNav')

class BrowseNavModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    global_menu: GlobalMenu = Field(..., alias='globalMenu')
    _raw_input: Any = PrivateAttr(default=None)

    @model_validator(mode='wrap')
    @classmethod
    def _capture_raw_input(cls, data: Any, handler: ModelWrapValidatorHandler[Self]) -> Self:
        """Validate the model and keep the input it was built from."""
        model = handler(data)
        model._raw_input = data
        return model

    @property
    def raw_input(self) -> Any:
        """The input this model was validated from, as it was handed over."""
        return self._raw_input
