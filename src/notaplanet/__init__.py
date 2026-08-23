# TODO: Validate
"""Contains the NotAPlanet class."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from logging import NullHandler, getLogger
from time import monotonic, sleep
from typing import Any

from get_around import GetAround

from notaplanet.categories import Categories
from notaplanet.exceptions import HTTPError, ResourceNotFoundError, UnknownServerError
from notaplanet.items import Items
from notaplanet.search import Search
from notaplanet.seasons import Seasons

logger = getLogger(__name__)
logger.addHandler(NullHandler())

APP_NAME = "web"
APP_VERSION = "9.22.0"
DEVICE_TYPE = "web"
DEVICE_MAKE = "firefox"
DEVICE_MODEL = "web"
DEVICE_VERSION = "153.0.0"
"""What the web player says it is, which is Firefox on Windows."""

FALLBACK_SERVERS = {
    "vod": "https://service-vod.clusters.pluto.tv",
    "search": "https://service-media-search.clusters.pluto.tv",
}
"""Used if the boot response ever stops reporting a host that is known to exist."""

DEFAULT_HEADERS = {
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
}


# TODO: Validate
class NotAPlanet:
    """Pluto TV API wrapper."""

    # TODO: Validate
    def __init__(
        self,
        get_around_client: GetAround | None = None,
        locale: str = "en",
        sleep_time: float = 0,
    ) -> None:
        """Initializes the NotAPlanet client.

        The client holds one attribute per endpoint, so `client.seasons(id)`
        looks the seasons of a series up and `client.seasons.download(id)` and
        `client.seasons.load(data)` are the halves of it.
        """
        self.get_around_client = get_around_client or GetAround()
        self.locale = locale
        self.sleep_time = sleep_time
        self.client_id = str(uuid.uuid4())

        self._session_token_value = ""
        self._servers: dict[str, str] = {}
        self._session_expires_at = datetime.now(tz=UTC)

        self.categories = Categories(self)
        self.items = Items(self)
        self.search = Search(self)
        self.seasons = Seasons(self)

    # TODO: Validate
    @property
    def _session_token(self) -> str:
        self._refresh_session_if_needed()
        return self._session_token_value

    # TODO: Validate
    def server_url(self, server: str) -> str:
        """Return the host for a service, as reported by the boot response.

        Raises:
            UnknownServerError: If neither the boot response nor the fallbacks
                have a host for `server`.
        """
        self._refresh_session_if_needed()
        url = self._servers.get(server) or FALLBACK_SERVERS.get(server)
        if not url:
            raise UnknownServerError(server, self._servers)
        return url

    # TODO: Validate
    def _refresh_session_if_needed(self) -> None:
        expired = self._session_expires_at < datetime.now(tz=UTC)
        if not self._session_token_value or expired:
            self._download_session()

    # TODO: Validate
    def _download_session(self) -> None:
        """Download an anonymous session and the hosts it is good for."""
        logger.debug("Downloading session:")
        start = monotonic()
        response = self.get_around_client.get(
            "https://boot.pluto.tv/v4/start",
            params={
                "appName": APP_NAME,
                "appVersion": APP_VERSION,
                "deviceVersion": DEVICE_VERSION,
                "deviceModel": DEVICE_MODEL,
                "deviceMake": DEVICE_MAKE,
                "deviceType": DEVICE_TYPE,
                "clientID": self.client_id,
                "clientModelNumber": "1.0.0",
                "serverSideAds": "false",
                "drmCapabilities": "widevine:L3",
                "blockingMode": "",
                "notificationVersion": "1",
                "appLaunchCount": "0",
                "clientTime": datetime.now(tz=UTC).isoformat(timespec="milliseconds"),
            },
            headers=DEFAULT_HEADERS,
        )
        if response.status_code != HTTPStatus.OK:
            raise HTTPError(response.status_code, response.text)

        logger.debug("Downloaded session (%.4f s)", monotonic() - start)

        parsed = response.json()
        self._session_token_value = parsed["sessionToken"]
        self._servers = parsed.get("servers") or {}
        self._session_expires_at = datetime.now(tz=UTC) + timedelta(
            seconds=parsed["refreshInSec"],
        )

    # TODO: Validate
    def download(
        self,
        server: str,
        endpoint: str,
        params: dict[str, Any],
        log_id: str,
    ) -> str:
        """Downloads from the API and returns the body as it was served.

        Raises:
            ResourceNotFoundError: If the API answers a 404, which is what it
                says for an id it has nothing under.
            HTTPError: If the request is answered with any other non-200.
        """
        headers = {
            **DEFAULT_HEADERS,
            "authorization": f"Bearer {self._session_token}",
        }

        logger.debug("Downloading: %s", log_id)
        url = f"{self.server_url(server)}/{endpoint}"
        start = monotonic()
        response = self.get_around_client.get(url, params=params, headers=headers)

        if response.status_code != HTTPStatus.OK:
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise ResourceNotFoundError(response.status_code, response.text)
            raise HTTPError(response.status_code, response.text)

        logger.debug("Downloaded %s (%.4f s)", log_id, monotonic() - start)
        sleep(self.sleep_time)
        return response.text
