from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, ConfigDict, Field

class AutocompleteItem(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    text: str | Any = Field(default=None, union_mode='left_to_right')

class Suggestions(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    autocomplete: list[AutocompleteItem] | Any = Field(default=None, union_mode='left_to_right')

class DistributeAs(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    avod: bool | Any = Field(None, alias='AVOD', union_mode='left_to_right')

class Datum(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    slug: str | Any = Field(default=None, union_mode='left_to_right')
    name: str | Any = Field(default=None, union_mode='left_to_right')
    type: str | Any = Field(default=None, union_mode='left_to_right')
    language: str | Any = Field(default=None, union_mode='left_to_right')
    number: int | Any = Field(default=None, union_mode='left_to_right')
    rating: str | Any = Field(default=None, union_mode='left_to_right')
    distribute_as: DistributeAs | Any = Field(None, alias='distributeAs', union_mode='left_to_right')

class Image(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    path: str | Any = Field(default=None, union_mode='left_to_right')
    title: str | Any = Field(default=None, union_mode='left_to_right')

class TrendingItem(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    slug: str | Any = Field(default=None, union_mode='left_to_right')
    name: str | Any = Field(default=None, union_mode='left_to_right')
    type: str | Any = Field(default=None, union_mode='left_to_right')
    language: str | Any = Field(default=None, union_mode='left_to_right')
    images: list[Image] | Any = Field(default=None, union_mode='left_to_right')
    number: int | Any = Field(default=None, union_mode='left_to_right')
    distribute_as: DistributeAs | Any = Field(None, alias='distributeAs', union_mode='left_to_right')
    rating: str | Any = Field(default=None, union_mode='left_to_right')
    season: int | Any = Field(default=None, union_mode='left_to_right')

class SearchModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    suggestions: Suggestions | Any = Field(default=None, union_mode='left_to_right')
    data: list[Datum] | Any = Field(default=None, union_mode='left_to_right')
    trending: list[TrendingItem] | Any = Field(default=None, union_mode='left_to_right')
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
