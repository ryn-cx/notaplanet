from typing import Any, Self
from pydantic import ModelWrapValidatorHandler, PrivateAttr, model_validator
from pydantic import ConfigDict
from pydantic import BaseModel, Field

class HubCarousel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    position: str
    token: str
    carousel_presentation_style: str = Field(..., alias='carouselPresentationStyle')
    carousel_id: str = Field(..., alias='carouselId')
    is_content_highlight_enabled: bool = Field(..., alias='isContentHighlightEnabled')
    title: str
    model: str
    display_title: None = Field(..., alias='displayTitle')
    href: str
    carousel_type: str = Field(..., alias='carouselType')

class HubModel(BaseModel):
    model_config = ConfigDict(defer_build=True)
    success: None
    hub_id: int = Field(..., alias='hubId')
    title: str
    hub_slug: str = Field(..., alias='hubSlug')
    type: str
    hero_token: None = Field(..., alias='heroToken')
    marquee_token: None = Field(..., alias='marqueeToken')
    hub_carousels: list[HubCarousel] = Field(..., alias='hubCarousels')
    page_type: str = Field(..., alias='pageType')
    region: str
    locale: str
    user_state: list[str] = Field(..., alias='userState')
    live_on_date: int = Field(..., alias='liveOnDate')
    start: int
    rows: int
    total: int
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
