# TODO: Validate
"""Contains the NotAPlanet class."""

import time
import uuid
from datetime import UTC, datetime, timedelta
from http import HTTPStatus
from logging import NullHandler, getLogger
from typing import Any

from get_around import GetAround

from notaplanet.categories import Categories
from notaplanet.exceptions import HTTPError, ResourceNotFoundError, UnknownServerError
from notaplanet.items import Items
from notaplanet.search import Search
from notaplanet.seasons import Seasons

logger = getLogger(__name__)
logger.addHandler(NullHandler())

# Anonymous sessions are handed out by the boot service, which also reports the
# regional hosts every other request has to be sent to.
BOOT_URL = "https://boot.pluto.tv/v4/start"

# Values chosen to match Firefox on Windows, which is what the web player sends.
APP_NAME = "web"
APP_VERSION = "9.22.0"
DEVICE_TYPE = "web"
DEVICE_MAKE = "firefox"
DEVICE_MODEL = "web"
DEVICE_VERSION = "153.0.0"

# Used if the boot response ever stops reporting a host that is known to exist.
FALLBACK_SERVERS = {
    "vod": "https://service-vod.clusters.pluto.tv",
    "search": "https://service-media-search.clusters.pluto.tv",
}

DEFAULT_HEADERS = {
    "origin": "https://pluto.tv",
    "referer": "https://pluto.tv/",
}


class NotAPlanet:
    """Pluto TV API wrapper."""

    def __init__(
        self,
        get_around_client: GetAround | None = None,
        locale: str = "en",
    ) -> None:
        """Initializes the NotAPlanet client."""
        self.locale = locale
        self.get_around_client = get_around_client or GetAround()
        self.client_id = str(uuid.uuid4())
        self._session_token_value = ""
        self._servers: dict[str, str] = {}
        self._session_expires_at = datetime.now(tz=UTC)

        self.seasons = Seasons(self)
        self.items = Items(self)
        self.categories = Categories(self)
        self.search = Search(self)

    @property
    def _session_token(self) -> str:
        self._refresh_session_if_needed()
        return self._session_token_value

    def server_url(self, server: str) -> str:
        """Returns the host for a service, as reported by the boot response."""
        self._refresh_session_if_needed()
        url = self._servers.get(server) or FALLBACK_SERVERS.get(server)
        if not url:
            raise UnknownServerError(server, self._servers)
        return url

    def _refresh_session_if_needed(self) -> None:
        expired = self._session_expires_at < datetime.now(tz=UTC)
        if not self._session_token_value or expired:
            self._download_session()

    def _download_session(self) -> None:
        logger.debug("Downloading session:")
        start = time.monotonic()
        response = self.get_around_client.get(
            BOOT_URL,
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

        logger.debug("Downloaded session (%.4f s)", time.monotonic() - start)

        parsed = response.json()
        self._session_token_value = parsed["sessionToken"]
        self._servers = parsed.get("servers") or {}
        self._session_expires_at = datetime.now(tz=UTC) + timedelta(
            seconds=parsed["refreshInSec"],
        )

    def download(
        self,
        server: str,
        endpoint: str,
        params: dict[str, Any],
        log_id: str,
    ) -> Any:  # noqa: ANN401 - Some endpoints return a JSON array.
        """Downloads from the API."""
        url = f"{self.server_url(server)}/{endpoint}"
        headers = {
            **DEFAULT_HEADERS,
            "authorization": f"Bearer {self._session_token}",
        }

        logger.debug("Downloading: %s", log_id)
        start = time.monotonic()
        response = self.get_around_client.get(url, params=params, headers=headers)

        if response.status_code != HTTPStatus.OK:
            if response.status_code == HTTPStatus.NOT_FOUND:
                raise ResourceNotFoundError(response.status_code, response.text)
            raise HTTPError(response.status_code, response.text)

        logger.debug("Downloaded %s (%.4f s)", log_id, time.monotonic() - start)
        return response.json()
