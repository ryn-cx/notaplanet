# TODO: Validate
import pytest
from get_around import build_client_automatically

from notaplanet import NotAPlanet


# TODO: Validate
@pytest.fixture(scope="session")
def client() -> NotAPlanet:
    return NotAPlanet(build_client_automatically())
