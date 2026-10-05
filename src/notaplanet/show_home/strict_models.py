from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from uuid import UUID
from pydantic import BaseModel, Field

class ShowAssets(BaseModel):
    model_config = ConfigDict(defer_build=True)
    filepath_video_endcard_show_image: str

class Season(BaseModel):
    model_config = ConfigDict(defer_build=True)
    season_num: str = Field(..., alias='seasonNum')
    total_count: int = Field(..., alias='totalCount')

class RegionalRating(BaseModel):
    model_config = ConfigDict(defer_build=True)
    rating_icon: None = Field(..., alias='ratingIcon')
    rating: str
    disclaimer: None

class Show(BaseModel):
    model_config = ConfigDict(defer_build=True)
    id: str
    slug: str
    title: str
    show_assets: ShowAssets = Field(..., alias='showAssets')
    logo: str
    callout: str
    premiere_date: str = Field(..., alias='premiereDate')
    description: str
    short_description: str = Field(..., alias='shortDescription')
    long_description: str = Field(..., alias='longDescription')
    genre: str
    category: str
    brand: None
    brand_url: str = Field(..., alias='brandUrl')
    num_seasons: int = Field(..., alias='numSeasons')
    show_episode_guide_link: bool = Field(..., alias='showEpisodeGuideLink')
    is_locked: bool = Field(..., alias='isLocked')
    show_episode_title: str = Field(..., alias='showEpisodeTitle')
    show_episode_id: str = Field(..., alias='showEpisodeId')
    seasons: list[Season]
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
    include_version: bool | None = Field(..., alias='includeVersion')
    token: str
    carousel_type: str = Field(..., alias='carouselType')

class ShowHomeModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    show: Show
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
