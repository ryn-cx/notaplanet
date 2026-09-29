from typing import Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from typing import Any
from pydantic import BaseModel, ConfigDict, Field

class HubCarousel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    position: str | Any = Field(default=None, union_mode='left_to_right')
    token: str | Any = Field(default=None, union_mode='left_to_right')
    carousel_presentation_style: str | Any = Field(None, alias='carouselPresentationStyle', union_mode='left_to_right')
    carousel_id: str | Any = Field(None, alias='carouselId', union_mode='left_to_right')
    is_content_highlight_enabled: bool | Any = Field(None, alias='isContentHighlightEnabled', union_mode='left_to_right')
    title: str | Any = Field(default=None, union_mode='left_to_right')
    model: str | Any = Field(default=None, union_mode='left_to_right')
    display_title: Any | None = Field(None, alias='displayTitle')
    href: str | Any = Field(default=None, union_mode='left_to_right')
    carousel_type: str | Any = Field(None, alias='carouselType', union_mode='left_to_right')

class HubModel(BaseModel):
    model_config = ConfigDict(extra='ignore', defer_build=True)
    success: Any | None = None
    hub_id: int | Any = Field(None, alias='hubId', union_mode='left_to_right')
    title: str | Any = Field(default=None, union_mode='left_to_right')
    hub_slug: str | Any = Field(None, alias='hubSlug', union_mode='left_to_right')
    type: str | Any = Field(default=None, union_mode='left_to_right')
    hero_token: Any | None = Field(None, alias='heroToken')
    marquee_token: Any | None = Field(None, alias='marqueeToken')
    hub_carousels: list[HubCarousel] | Any = Field(None, alias='hubCarousels', union_mode='left_to_right')
    page_type: str | Any = Field(None, alias='pageType', union_mode='left_to_right')
    region: str | Any = Field(default=None, union_mode='left_to_right')
    locale: str | Any = Field(default=None, union_mode='left_to_right')
    user_state: list[str] | Any = Field(None, alias='userState', union_mode='left_to_right')
    live_on_date: int | Any = Field(None, alias='liveOnDate', union_mode='left_to_right')
    start: int | Any = Field(default=None, union_mode='left_to_right')
    rows: int | Any = Field(default=None, union_mode='left_to_right')
    total: int | Any = Field(default=None, union_mode='left_to_right')
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
