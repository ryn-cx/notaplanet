from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from uuid import UUID
from pydantic import AwareDatetime, BaseModel, ConfigDict, Field

class MovieAssets(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    filepath_movie_keep_watching: str | Any = Field(default=None, union_mode='left_to_right')

class RegionalRating(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    rating_icon: str | Any = Field(None, alias='ratingIcon', union_mode='left_to_right')
    rating: str | Any = Field(default=None, union_mode='left_to_right')
    disclaimer: Any | None = None

class Movie(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    title: str | Any = Field(default=None, union_mode='left_to_right')
    movie_assets: MovieAssets | Any = Field(None, alias='movieAssets', union_mode='left_to_right')
    logo: str | Any = Field(default=None, union_mode='left_to_right')
    callout: str | Any = Field(default=None, union_mode='left_to_right')
    content_id: str | Any = Field(None, alias='contentId', union_mode='left_to_right')
    premiere_date: AwareDatetime | Any = Field(None, alias='premiereDate', union_mode='left_to_right')
    description: str | Any = Field(default=None, union_mode='left_to_right')
    short_description: str | Any = Field(None, alias='shortDescription', union_mode='left_to_right')
    long_description: str | Any = Field(None, alias='longDescription', union_mode='left_to_right')
    genre: str | Any = Field(default=None, union_mode='left_to_right')
    category: str | Any = Field(default=None, union_mode='left_to_right')
    brand: str | Any = Field(default=None, union_mode='left_to_right')
    region: str | Any = Field(default=None, union_mode='left_to_right')
    brand_url: Any | None = Field(None, alias='brandUrl')
    num_seasons: int | Any = Field(None, alias='numSeasons', union_mode='left_to_right')
    show_episode_guide_link: bool | Any = Field(None, alias='showEpisodeGuideLink', union_mode='left_to_right')
    is_locked: bool | Any = Field(None, alias='isLocked', union_mode='left_to_right')
    directors: list[str] | Any = Field(default=None, union_mode='left_to_right')
    pub_date: AwareDatetime | Any = Field(None, alias='pubDate', union_mode='left_to_right')
    seasons: list[Any] | Any = Field(default=None, union_mode='left_to_right')
    regional_ratings: list[RegionalRating] | Any = Field(None, alias='regionalRatings', union_mode='left_to_right')
    is_kids_content: bool | Any = Field(None, alias='isKidsContent', union_mode='left_to_right')

class CarouselConfig(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    title: str | Any = Field(default=None, union_mode='left_to_right')
    position: Any | None = None
    model: str | Any = Field(default=None, union_mode='left_to_right')
    orientation: str | Any = Field(default=None, union_mode='left_to_right')
    carousel_id: UUID | Any = Field(None, alias='carouselId', union_mode='left_to_right')
    carousel_presentation_style: str | Any = Field(None, alias='carouselPresentationStyle', union_mode='left_to_right')
    include_version: bool | Any = Field(None, alias='includeVersion', union_mode='left_to_right')
    token: str | Any = Field(default=None, union_mode='left_to_right')
    carousel_type: str | Any = Field(None, alias='carouselType', union_mode='left_to_right')
    is_content_highlight_enabled: bool | Any = Field(None, alias='isContentHighlightEnabled', union_mode='left_to_right')

class MovieDetailModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    movie: Movie | Any = Field(default=None, union_mode='left_to_right')
    carousel_configs: list[CarouselConfig] | Any = Field(None, alias='carouselConfigs', union_mode='left_to_right')
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
