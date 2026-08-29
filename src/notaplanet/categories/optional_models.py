from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

class MainCategory(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    category_id: str | None = Field(None, alias='categoryID')

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
    producers: list[str] | None = None
    original_release_date: AwareDatetime | None = Field(None, alias='originalReleaseDate')
    writers: list[str] | None = None

class Item(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_id: str | None = Field(None, alias='_id')
    series_id: str | None = Field(None, alias='seriesID')
    slug: str | None = None
    name: str | None = None
    summary: str | None = None
    description: str | None = None
    duration: int | None = None
    original_content_duration: int | None = Field(None, alias='originalContentDuration')
    allotment: int | None = None
    rating: str | None = None
    featured_image: FeaturedImage | None = Field(None, alias='featuredImage')
    genre: str | None = None
    type: str | None = None
    seasons_numbers: list[int] | None = Field(None, alias='seasonsNumbers')
    stitched: Stitched | None = None
    covers: list[Cover] | None = None
    poster16_9: Poster169 | None = None
    clip: Clip | None = None
    avail: dict[str, Any] | None = None
    cc: bool | None = None
    ad: bool | None = None
    rating_descriptors: list[str] | None = Field(None, alias='ratingDescriptors')

class Category(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_id: str | None = Field(None, alias='_id')
    name: str | None = None
    pluto_office_only: bool | None = Field(None, alias='plutoOfficeOnly')
    page: int | None = None
    offset: int | None = None
    total_items_count: int | None = Field(None, alias='totalItemsCount')
    main_categories: list[MainCategory] | None = Field(None, alias='mainCategories')
    items: list[Item] | None = None
    hero_carousel: bool | None = None

class CategoriesModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    offset: int | None = None
    page: int | None = None
    total_categories: int | None = Field(None, alias='totalCategories')
    total_pages: int | None = Field(None, alias='totalPages')
    categories: list[Category] | None = None
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
