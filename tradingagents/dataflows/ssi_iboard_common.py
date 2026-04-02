"""SSI iBoard HTTP client with Cloudflare cookie authentication.

Reads cookie credentials from environment variables:
    SSI_CF_CLEARANCE   — Cloudflare cf_clearance cookie
    SSI_ID_TOKEN       — OpenID id_token cookie
    SSI_TOKEN          — SSI authorization token cookie

Usage::

    from .ssi_iboard_common import get_session, SSI_BASE_URL
    session = get_session()
    resp = session.get(f"{SSI_BASE_URL}/stock/group/VN30")
"""

import os
import requests

SSI_BASE_URL = "https://iboard-query.ssi.com.vn"

_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    "Origin": "https://iboard.ssi.com.vn",
    "Referer": "https://iboard.ssi.com.vn/",
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
}


def get_session() -> requests.Session:
    """Build a requests.Session pre-loaded with SSI iBoard cookies from env."""
    session = requests.Session()
    session.headers.update(_HEADERS)

    cf_clearance = os.getenv("SSI_CF_CLEARANCE", "")
    id_token = os.getenv("SSI_ID_TOKEN", "")
    ssi_token = os.getenv("SSI_TOKEN", "")

    if not any([cf_clearance, id_token, ssi_token]):
        raise EnvironmentError(
            "SSI iBoard cookies not configured. "
            "Set SSI_CF_CLEARANCE, SSI_ID_TOKEN, and SSI_TOKEN in your .env file. "
            "See .env.example for instructions."
        )

    cookies: dict[str, str] = {}
    if cf_clearance:
        cookies["cf_clearance"] = cf_clearance
    if id_token:
        # The actual cookie name on iboard.ssi.com.vn is "sso.id_token"
        cookies["sso.id_token"] = id_token
    if ssi_token:
        cookies["token"] = ssi_token

    session.cookies.update(cookies)
    return session


def ssi_get(path: str, params: dict | None = None) -> dict:
    """Make an authenticated GET request to the SSI iBoard API.

    Args:
        path: URL path relative to SSI_BASE_URL (e.g. "/stock/group/VN30").
        params: Optional query parameters.

    Returns:
        Parsed JSON response dict.

    Raises:
        requests.HTTPError: On non-2xx responses.
        EnvironmentError: If cookies are not configured.
    """
    session = get_session()
    url = f"{SSI_BASE_URL}{path}"
    response = session.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()
