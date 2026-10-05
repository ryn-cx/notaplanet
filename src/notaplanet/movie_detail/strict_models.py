from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from typing import Any
from uuid import UUID
from pydantic import AwareDatetime, BaseModel, Field

class MovieAssets(BaseModel):
    model_config = ConfigDict(defer_build=True)
    filepath_movie_keep_watching: str

class RegionalRating(BaseModel):
    model_config = ConfigDict(defer_build=True)
    rating_icon: str = Field(..., alias='ratingIcon')
    rating: str
    disclaimer: None

class Movie(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    title: str
    movie_assets: MovieAssets = Field(..., alias='movieAssets')
    logo: str
    callout: str
    content_id: str = Field(..., alias='contentId')
    premiere_date: AwareDatetime = Field(..., alias='premiereDate')
    description: str
    short_description: str = Field(..., alias='shortDescription')
    long_description: str = Field(..., alias='longDescription')
    genre: str
    category: str
    brand: str
    region: str
    brand_url: None = Field(..., alias='brandUrl')
    num_seasons: int = Field(..., alias='numSeasons')
    show_episode_guide_link: bool = Field(..., alias='showEpisodeGuideLink')
    is_locked: bool = Field(..., alias='isLocked')
    directors: list[str]
    pub_date: AwareDatetime = Field(..., alias='pubDate')
    seasons: list[None]
    regional_ratings: list[RegionalRating] = Field(..., alias='regionalRatings')
    is_kids_content: bool = Field(..., alias='isKidsContent')

class CarouselConfig(BaseModel):
    model_config = ConfigDict(defer_build=True)
    title: str
    position: None
    model: str
    orientation: str
    carousel_id: UUID = Field(..., alias='carouselId')
    carousel_presentation_style: str = Field(..., alias='carouselPresentationStyle')
    include_version: bool = Field(..., alias='includeVersion')
    token: str
    carousel_type: str = Field(..., alias='carouselType')
    is_content_highlight_enabled: bool = Field(..., alias='isContentHighlightEnabled')

class MovieDetailModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    movie: Movie
    carousel_configs: list[CarouselConfig] = Field(..., alias='carouselConfigs')
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
