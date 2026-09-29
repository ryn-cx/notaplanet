from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, ConfigDict, Field

class ShowBrowseNavItem(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    label: str | Any = Field(default=None, union_mode='left_to_right')
    slug: str | Any = Field(default=None, union_mode='left_to_right')
    type: str | Any = Field(default=None, union_mode='left_to_right')
    href: str | Any = Field(default=None, union_mode='left_to_right')
    locale: str | Any = Field(default=None, union_mode='left_to_right')

class MovieBrowseNavItem(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    label: str | Any = Field(default=None, union_mode='left_to_right')
    slug: str | Any = Field(default=None, union_mode='left_to_right')
    type: str | Any = Field(default=None, union_mode='left_to_right')
    href: str | Any = Field(default=None, union_mode='left_to_right')
    locale: str | Any = Field(default=None, union_mode='left_to_right')

class GlobalMenu(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    show_browse_nav: list[ShowBrowseNavItem] | Any = Field(None, alias='showBrowseNav', union_mode='left_to_right')
    movie_browse_nav: list[MovieBrowseNavItem] | Any = Field(None, alias='movieBrowseNav', union_mode='left_to_right')

class BrowseNavModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    global_menu: GlobalMenu | Any = Field(None, alias='globalMenu', union_mode='left_to_right')
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
