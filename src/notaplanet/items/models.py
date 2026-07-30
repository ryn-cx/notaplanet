from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict, Field

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

class Category(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str

class Poster169(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    path: str

class Avail(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    end_date: AwareDatetime | None = Field(None, alias='endDate')

class Clip(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    actors: list[str]
    directors: list[str]
    producers: list[str]
    original_release_date: AwareDatetime = Field(..., alias='originalReleaseDate')

class Item(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
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
    avail: Avail
    series_id: str | None = Field(None, alias='seriesID')
    duration: int | None = None
    allotment: int | None = None
    clip: Clip | None = None
    cc: bool | None = None

class ItemsModel(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    items: list[Item]
