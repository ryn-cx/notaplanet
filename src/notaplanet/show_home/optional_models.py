from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class ShowAssets(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    filepath_video_endcard_show_image: str | Any = Field(default=None, union_mode='left_to_right')

class Season(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    season_num: str | Any = Field(None, alias='seasonNum', union_mode='left_to_right')
    total_count: int | Any = Field(None, alias='totalCount', union_mode='left_to_right')

class RegionalRating(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    rating_icon: Any | None = Field(None, alias='ratingIcon')
    rating: str | Any = Field(default=None, union_mode='left_to_right')
    disclaimer: Any | None = None

class Show(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    id: str | Any = Field(default=None, union_mode='left_to_right')
    slug: str | Any = Field(default=None, union_mode='left_to_right')
    title: str | Any = Field(default=None, union_mode='left_to_right')
    show_assets: ShowAssets | Any = Field(None, alias='showAssets', union_mode='left_to_right')
    logo: str | Any = Field(default=None, union_mode='left_to_right')
    callout: str | Any = Field(default=None, union_mode='left_to_right')
    premiere_date: str | Any = Field(None, alias='premiereDate', union_mode='left_to_right')
    description: str | Any = Field(default=None, union_mode='left_to_right')
    short_description: str | Any = Field(None, alias='shortDescription', union_mode='left_to_right')
    long_description: str | Any = Field(None, alias='longDescription', union_mode='left_to_right')
    genre: str | Any = Field(default=None, union_mode='left_to_right')
    category: str | Any = Field(default=None, union_mode='left_to_right')
    brand: Any | None = None
    brand_url: str | Any = Field(None, alias='brandUrl', union_mode='left_to_right')
    num_seasons: int | Any = Field(None, alias='numSeasons', union_mode='left_to_right')
    show_episode_guide_link: bool | Any = Field(None, alias='showEpisodeGuideLink', union_mode='left_to_right')
    is_locked: bool | Any = Field(None, alias='isLocked', union_mode='left_to_right')
    show_episode_title: str | Any = Field(None, alias='showEpisodeTitle', union_mode='left_to_right')
    show_episode_id: str | Any = Field(None, alias='showEpisodeId', union_mode='left_to_right')
    seasons: list[Season] | Any = Field(default=None, union_mode='left_to_right')
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

class ShowHomeModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    show: Show | Any = Field(default=None, union_mode='left_to_right')
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
