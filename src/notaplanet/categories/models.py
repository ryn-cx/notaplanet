from datetime import timedelta
from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict, Field

class MainCategory(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    category_id: str = Field(..., alias='categoryID')

class FeaturedImage(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    path: str

class Path(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    type: str
    path: str

class Stitched(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    paths: list[Path] | None = None

class Cover(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    aspect_ratio: str = Field(..., alias='aspectRatio')
    url: str

class Poster169(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    path: str

class Clip(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    actors: list[str] | None = None
    directors: list[str] | None = None
    producers: list[str] | None = None
    original_release_date: AwareDatetime | None = Field(None, alias='originalReleaseDate')
    writers: list[str] | None = None

class Avail(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    end_date: AwareDatetime | None = Field(None, alias='endDate')
    start_date: AwareDatetime | None = Field(None, alias='startDate')

class Item(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    field_id: str = Field(..., alias='_id')
    series_id: str | None = Field(None, alias='seriesID')
    slug: str
    name: timedelta | str = Field(union_mode='left_to_right')
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
    poster16_9: Poster169
    clip: Clip | None = None
    avail: Avail
    cc: bool | None = None
    ad: bool | None = None
    rating_descriptors: list[str] | None = Field(None, alias='ratingDescriptors')
    entitlements: list[str] | None = None
    kids_mode: bool | None = Field(None, alias='kidsMode')

class Category(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    field_id: str = Field(..., alias='_id')
    name: str
    pluto_office_only: bool = Field(..., alias='plutoOfficeOnly')
    page: int
    offset: int
    total_items_count: int = Field(..., alias='totalItemsCount')
    main_categories: list[MainCategory] = Field(..., alias='mainCategories')
    items: list[Item]
    hero_carousel: bool | None = None
    kids_mode: bool | None = Field(None, alias='kidsMode')

class CategoriesModel(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    offset: int
    page: int
    total_categories: int = Field(..., alias='totalCategories')
    total_pages: int = Field(..., alias='totalPages')
    categories: list[Category]
