from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from typing import Any
from pydantic import AwareDatetime, BaseModel, Field

class FeaturedImage(BaseModel):
    model_config = ConfigDict(defer_build=True)
    path: str

class Path(BaseModel):
    model_config = ConfigDict(defer_build=True)
    type: str
    path: str

class Stitched(BaseModel):
    model_config = ConfigDict(defer_build=True)
    paths: list[Path]

class Cover(BaseModel):
    model_config = ConfigDict(defer_build=True)
    aspect_ratio: str = Field(..., alias='aspectRatio')
    url: str

class Poster169(BaseModel):
    model_config = ConfigDict(defer_build=True)
    path: str

class Clip(BaseModel):
    model_config = ConfigDict(defer_build=True)
    actors: list[str] | None = None
    directors: list[str] | None = None
    writers: list[str] | None = None
    producers: list[str] | None = None
    original_release_date: AwareDatetime = Field(..., alias='originalReleaseDate')

class Episode(BaseModel):
    model_config = ConfigDict(defer_build=True)
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
    cc: bool | None = None
    clip: Clip | None = None

class Season(BaseModel):
    model_config = ConfigDict(defer_build=True)
    episodes: list[Episode]
    number: int

class SeasonsModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
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
