from good_ass_pydantic_integrator import GAPIBaseModel
from pydantic import AwareDatetime, ConfigDict, Field

class AutocompleteItem(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    text: str

class Suggestions(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    autocomplete: list[AutocompleteItem]

class DistributeAs(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    avod: bool = Field(..., alias='AVOD')

class Logo(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    path: str

class Channel(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    slug: str
    name: str
    number: int
    logo: Logo

class Datum(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    slug: str
    name: str
    type: str
    language: str
    number: int | None = None
    rating: str | None = None
    distribute_as: DistributeAs | None = Field(None, alias='distributeAs')
    start: AwareDatetime | None = None
    stop: AwareDatetime | None = None
    channel: Channel | None = None

class SearchModel(GAPIBaseModel):
    model_config = ConfigDict(extra='forbid')
    suggestions: Suggestions
    data: list[Datum]
