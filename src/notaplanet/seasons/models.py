from typing import Any
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
    paths: list[Path]

class Cover(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    aspect_ratio: str = Field(..., alias='aspectRatio')
    url: str

class Poster169(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    path: str

class Clip(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    actors: list[str]
    directors: list[str] | None = None
    original_release_date: AwareDatetime = Field(..., alias='originalReleaseDate')
    producers: list[str] | None = None
    writers: list[str] | None = None

class Episode(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
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

class Season(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    episodes: list[Episode]
    number: int

class SeasonsModel(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
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
