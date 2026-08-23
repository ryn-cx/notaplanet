from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import AwareDatetime, BaseModel, Field

class FeaturedImage(BaseModel):
    path: str

class Path(BaseModel):
    type: str
    path: str

class Stitched(BaseModel):
    paths: list[Path]

class Cover(BaseModel):
    aspect_ratio: str = Field(..., alias='aspectRatio')
    url: str

class Poster169(BaseModel):
    path: str

class Clip(BaseModel):
    actors: list[str]
    directors: list[str]
    writers: list[str]
    producers: list[str]
    original_release_date: AwareDatetime = Field(..., alias='originalReleaseDate')

class Episode(BaseModel):
    field_id: str = Field(..., alias='_id')
    name: str
    description: str
    allotment: int
    rating: str
    slug: str
    duration: int
    original_content_duration: int = Field(..., alias='originalContentDuration')
    genre: str
    type: str
    number: int
    season: int
    stitched: Stitched
    covers: list[Cover]
    poster16_9: Poster169
    cc: bool
    clip: Clip

class Season(BaseModel):
    episodes: list[Episode]
    number: int

class SeasonsModel(BaseModel):
    field_id: str = Field(..., alias='_id')
    name: str
    summary: str
    description: str
    slug: str
    type: str
    rating: str
    featured_image: FeaturedImage = Field(..., alias='featuredImage')
    genre: str
    offset: int
    page: int
    seasons: list[Season]
    covers: list[Cover]
    poster16_9: Poster169
    avail: dict[str, Any]
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
