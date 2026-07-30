import pytest
from get_around import build_client_automatically

from notaplanet import NotAPlanet


@pytest.fixture(scope="session")
def client() -> NotAPlanet:
    return NotAPlanet(build_client_automatically())
