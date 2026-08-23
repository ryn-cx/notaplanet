from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import AwareDatetime, BaseModel, Field, RootModel

class FeaturedImage(BaseModel):
    path: str

class Path(BaseModel):
    type: str
    path: str

class Stitched(BaseModel):
    paths: list[Path] | None = None

class Cover(BaseModel):
    aspect_ratio: str = Field(..., alias='aspectRatio')
    url: str

class Category(BaseModel):
    id: str

class Poster169(BaseModel):
    path: str

class Clip(BaseModel):
    actors: list[str]
    directors: list[str]
    writers: list[str]
    producers: list[str]
    original_release_date: AwareDatetime = Field(..., alias='originalReleaseDate')

class ItemsModelItem(BaseModel):
    field_id: str = Field(..., alias='_id')
    slug: str
    name: str
    summary: str
    description: str
    original_content_duration: int = Field(..., alias='originalContentDuration')
    rating: str
    featured_image: FeaturedImage = Field(..., alias='featuredImage')
    genre: str
    type: str
    seasons_numbers: list[int] = Field(..., alias='seasonsNumbers')
    stitched: Stitched
    covers: list[Cover]
    categories: list[Category]
    poster16_9: Poster169
    avail: dict[str, Any]
    series_id: str | None = Field(None, alias='seriesID')
    duration: int | None = None
    allotment: int | None = None
    clip: Clip | None = None
    cc: bool | None = None

class ItemsModel(RootModel[list[ItemsModelItem]]):
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
