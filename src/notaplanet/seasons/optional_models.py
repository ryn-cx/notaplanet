from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

class FeaturedImage(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    path: str | None = None

class Path(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    type: str | None = None
    path: str | None = None

class Stitched(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    paths: list[Path] | None = None

class Cover(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    aspect_ratio: str | None = Field(None, alias='aspectRatio')
    url: str | None = None

class Poster169(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    path: str | None = None

class Clip(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    actors: list[str] | None = None
    directors: list[str] | None = None
    writers: list[str] | None = None
    producers: list[str] | None = None
    original_release_date: AwareDatetime | None = Field(None, alias='originalReleaseDate')

class Episode(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_id: str | None = Field(None, alias='_id')
    name: str | None = None
    description: str | None = None
    allotment: int | None = None
    rating: str | None = None
    slug: str | None = None
    duration: int | None = None
    original_content_duration: int | None = Field(None, alias='originalContentDuration')
    genre: str | None = None
    type: str | None = None
    number: int | None = None
    season: int | None = None
    stitched: Stitched | None = None
    covers: list[Cover] | None = None
    poster16_9: Poster169 | None = None
    cc: bool | None = None
    clip: Clip | None = None

class Season(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    episodes: list[Episode] | None = None
    number: int | None = None

class SeasonsModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_id: str | None = Field(None, alias='_id')
    name: str | None = None
    summary: str | None = None
    description: str | None = None
    slug: str | None = None
    type: str | None = None
    rating: str | None = None
    featured_image: FeaturedImage | None = Field(None, alias='featuredImage')
    genre: str | None = None
    offset: int | None = None
    page: int | None = None
    seasons: list[Season] | None = None
    covers: list[Cover] | None = None
    poster16_9: Poster169 | None = None
    avail: dict[str, Any] | None = None
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
