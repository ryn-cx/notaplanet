from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, ConfigDict, Field

class AutocompleteItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    text: str | None = None

class Suggestions(BaseModel):
    model_config = ConfigDict(extra='ignore')
    autocomplete: list[AutocompleteItem] | None = None

class DistributeAs(BaseModel):
    model_config = ConfigDict(extra='ignore')
    avod: bool | None = Field(None, alias='AVOD')

class Datum(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str | None = None
    slug: str | None = None
    name: str | None = None
    type: str | None = None
    language: str | None = None
    number: int | None = None
    rating: str | None = None
    distribute_as: DistributeAs | None = Field(None, alias='distributeAs')

class Image(BaseModel):
    model_config = ConfigDict(extra='ignore')
    path: str | None = None
    title: str | None = None

class TrendingItem(BaseModel):
    model_config = ConfigDict(extra='ignore')
    id: str | None = None
    slug: str | None = None
    name: str | None = None
    type: str | None = None
    language: str | None = None
    images: list[Image] | None = None
    number: int | None = None
    distribute_as: DistributeAs | None = Field(None, alias='distributeAs')
    rating: str | None = None
    season: int | None = None

class SearchModel(BaseModel):
    model_config = ConfigDict(extra='ignore')
    suggestions: Suggestions | None = None
    data: list[Datum] | None = None
    trending: list[TrendingItem] | None = None
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
