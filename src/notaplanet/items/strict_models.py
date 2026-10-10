from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from typing import Any
from pydantic import AwareDatetime, BaseModel, Field, RootModel

class FeaturedImage(BaseModel):
    model_config = ConfigDict(defer_build=True)
    path: str

class Path(BaseModel):
    model_config = ConfigDict(defer_build=True)
    type: str
    path: str

class Stitched(BaseModel):
    model_config = ConfigDict(defer_build=True)
    paths: list[Path] | None = None

class Cover(BaseModel):
    model_config = ConfigDict(defer_build=True)
    aspect_ratio: str = Field(..., alias='aspectRatio')
    url: str

class Category(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str

class Poster169(BaseModel):
    model_config = ConfigDict(defer_build=True)
    path: str

class Clip(BaseModel):
    model_config = ConfigDict(defer_build=True)
    actors: list[str] | None = None
    directors: list[str] | None = None
    writers: list[str] | None = None
    original_release_date: AwareDatetime | None = Field(None, alias='originalReleaseDate')
    producers: list[str] | None = None

class ItemsModelItem(BaseModel):
    model_config = ConfigDict(defer_build=True)
    field_id: str = Field(..., alias='_id')
    series_id: str | None = Field(None, alias='seriesID')
    slug: str
    name: str
    summary: str
    description: str
    duration: int | None = None
    original_content_duration: int = Field(..., alias='originalContentDuration')
    allotment: int | None = None
    rating: str
    featured_image: FeaturedImage = Field(..., alias='featuredImage')
    genre: str
    type: str
    seasons_numbers: list[int] = Field(..., alias='seasonsNumbers')
    stitched: Stitched
    covers: list[Cover]
    categories: list[Category]
    poster16_9: Poster169
    clip: Clip | None = None
    avail: dict[str, Any]
    cc: bool | None = None
    rating_descriptors: list[str] | None = Field(None, alias='ratingDescriptors')

class ItemsModel(RootModel[list[ItemsModelItem]]):
    model_config = ConfigDict(defer_build=True)
    root: list[ItemsModelItem]
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
