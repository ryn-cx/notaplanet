from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import BaseModel, Field

class AutocompleteItem(BaseModel):
    text: str

class Suggestions(BaseModel):
    autocomplete: list[AutocompleteItem]

class DistributeAs(BaseModel):
    avod: bool = Field(..., alias='AVOD')

class Datum(BaseModel):
    id: str
    slug: str
    name: str
    type: str
    language: str
    number: int | None = None
    rating: str | None = None
    distribute_as: DistributeAs | None = Field(None, alias='distributeAs')

class Image(BaseModel):
    path: str
    title: str

class TrendingItem(BaseModel):
    id: str
    slug: str
    name: str
    type: str
    language: str
    images: list[Image]
    number: int | None = None
    distribute_as: DistributeAs | None = Field(None, alias='distributeAs')
    rating: str | None = None
    season: int | None = None

class SearchModel(BaseModel):
    suggestions: Suggestions
    data: list[Datum]
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
