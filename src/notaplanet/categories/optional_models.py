from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

class MainCategory(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    category_id: str | Any = Field(None, alias='categoryID', union_mode='left_to_right')

class FeaturedImage(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    path: str | Any = Field(default=None, union_mode='left_to_right')

class Path(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    type: str | Any = Field(default=None, union_mode='left_to_right')
    path: str | Any = Field(default=None, union_mode='left_to_right')

class Stitched(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    paths: list[Path] | Any = Field(default=None, union_mode='left_to_right')

class Cover(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    aspect_ratio: str | Any = Field(None, alias='aspectRatio', union_mode='left_to_right')
    url: str | Any = Field(default=None, union_mode='left_to_right')

class Poster169(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    path: str | Any = Field(default=None, union_mode='left_to_right')

class Clip(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    actors: list[str] | Any = Field(default=None, union_mode='left_to_right')
    directors: list[str] | Any = Field(default=None, union_mode='left_to_right')
    producers: list[str] | Any = Field(default=None, union_mode='left_to_right')
    original_release_date: AwareDatetime | Any = Field(None, alias='originalReleaseDate', union_mode='left_to_right')
    writers: list[str] | Any = Field(default=None, union_mode='left_to_right')

class Item(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_id: str | Any = Field(None, alias='_id', union_mode='left_to_right')
    series_id: str | Any = Field(None, alias='seriesID', union_mode='left_to_right')
    slug: str | Any = Field(default=None, union_mode='left_to_right')
    name: str | Any = Field(default=None, union_mode='left_to_right')
    summary: str | Any = Field(default=None, union_mode='left_to_right')
    description: str | Any = Field(default=None, union_mode='left_to_right')
    duration: int | Any = Field(default=None, union_mode='left_to_right')
    original_content_duration: int | Any = Field(None, alias='originalContentDuration', union_mode='left_to_right')
    allotment: int | Any = Field(default=None, union_mode='left_to_right')
    rating: str | Any = Field(default=None, union_mode='left_to_right')
    featured_image: FeaturedImage | Any = Field(None, alias='featuredImage', union_mode='left_to_right')
    genre: str | Any = Field(default=None, union_mode='left_to_right')
    type: str | Any = Field(default=None, union_mode='left_to_right')
    seasons_numbers: list[int] | Any = Field(None, alias='seasonsNumbers', union_mode='left_to_right')
    stitched: Stitched | Any = Field(default=None, union_mode='left_to_right')
    covers: list[Cover] | Any = Field(default=None, union_mode='left_to_right')
    poster16_9: Poster169 | Any = Field(default=None, union_mode='left_to_right')
    clip: Clip | Any = Field(default=None, union_mode='left_to_right')
    avail: dict[str, Any] | Any = Field(default=None, union_mode='left_to_right')
    cc: bool | Any = Field(default=None, union_mode='left_to_right')
    ad: bool | Any = Field(default=None, union_mode='left_to_right')
    rating_descriptors: list[str] | Any = Field(None, alias='ratingDescriptors', union_mode='left_to_right')

class Category(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    field_id: str | Any = Field(None, alias='_id', union_mode='left_to_right')
    name: str | Any = Field(default=None, union_mode='left_to_right')
    pluto_office_only: bool | Any = Field(None, alias='plutoOfficeOnly', union_mode='left_to_right')
    page: int | Any = Field(default=None, union_mode='left_to_right')
    offset: int | Any = Field(default=None, union_mode='left_to_right')
    total_items_count: int | Any = Field(None, alias='totalItemsCount', union_mode='left_to_right')
    main_categories: list[MainCategory] | Any = Field(None, alias='mainCategories', union_mode='left_to_right')
    items: list[Item] | Any = Field(default=None, union_mode='left_to_right')
    hero_carousel: bool | Any = Field(default=None, union_mode='left_to_right')

class CategoriesModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    offset: int | Any = Field(default=None, union_mode='left_to_right')
    page: int | Any = Field(default=None, union_mode='left_to_right')
    total_categories: int | Any = Field(None, alias='totalCategories', union_mode='left_to_right')
    total_pages: int | Any = Field(None, alias='totalPages', union_mode='left_to_right')
    categories: list[Category] | Any = Field(default=None, union_mode='left_to_right')
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
