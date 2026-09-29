from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from datetime import time, timedelta
from pydantic import AwareDatetime, BaseModel, Field

class Datum(BaseModel):
    model_config = ConfigDict(defer_build=True)
    content_type: str = Field(..., alias='contentType')
    href: str
    id: str
    thumb: str
    tile_type: str = Field(..., alias='tileType')
    orientation: str
    title: time | timedelta | str = Field(union_mode='left_to_right')
    description: str
    genre: str
    movie_id: str | None = Field(None, alias='movieId')
    movie_duration: int | None = Field(None, alias='movieDuration')
    air_date: AwareDatetime | None = Field(None, alias='airDate')
    is_kids_content: bool = Field(..., alias='isKidsContent')
    thumb_landscape: str = Field(..., alias='thumbLandscape')
    rating: str | None = None
    num_seasons: int | None = Field(None, alias='numSeasons')
    premiere_date: AwareDatetime | str | None = Field(None, alias='premiereDate', union_mode='left_to_right')

class Result(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    title: str
    total: int
    rows: int
    skipped: int
    has_more: bool = Field(..., alias='hasMore')
    data: list[Datum]

class CarouselModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    success: bool
    result: Result
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
