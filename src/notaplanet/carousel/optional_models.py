from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from datetime import time, timedelta
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

class Datum(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    content_type: str | Any = Field(None, alias='contentType', union_mode='left_to_right')
    href: str | Any = Field(default=None, union_mode='left_to_right')
    id: str | Any = Field(default=None, union_mode='left_to_right')
    thumb: str | Any = Field(default=None, union_mode='left_to_right')
    tile_type: str | Any = Field(None, alias='tileType', union_mode='left_to_right')
    orientation: str | Any = Field(default=None, union_mode='left_to_right')
    title: time | timedelta | str | Any = Field(default=None, union_mode='left_to_right')
    description: str | Any = Field(default=None, union_mode='left_to_right')
    genre: str | Any = Field(default=None, union_mode='left_to_right')
    movie_id: str | Any = Field(None, alias='movieId', union_mode='left_to_right')
    movie_duration: int | Any = Field(None, alias='movieDuration', union_mode='left_to_right')
    air_date: AwareDatetime | Any = Field(None, alias='airDate', union_mode='left_to_right')
    is_kids_content: bool | Any = Field(None, alias='isKidsContent', union_mode='left_to_right')
    thumb_landscape: str | Any = Field(None, alias='thumbLandscape', union_mode='left_to_right')
    rating: str | Any = Field(default=None, union_mode='left_to_right')
    num_seasons: int | Any = Field(None, alias='numSeasons', union_mode='left_to_right')
    premiere_date: AwareDatetime | str | Any = Field(None, alias='premiereDate', union_mode='left_to_right')

class Result(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    title: str | Any = Field(default=None, union_mode='left_to_right')
    total: int | Any = Field(default=None, union_mode='left_to_right')
    rows: int | Any = Field(default=None, union_mode='left_to_right')
    skipped: int | Any = Field(default=None, union_mode='left_to_right')
    has_more: bool | Any = Field(None, alias='hasMore', union_mode='left_to_right')
    data: list[Datum] | Any = Field(default=None, union_mode='left_to_right')

class CarouselModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    success: bool | Any = Field(default=None, union_mode='left_to_right')
    result: Result | Any = Field(default=None, union_mode='left_to_right')
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
