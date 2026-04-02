"""ChatGPT Codex OAuth authentication for TradingAgents.

Implements the same PKCE OAuth flow used by OpenClaw/pi-ai to authenticate
with ChatGPT and obtain an access token for the Codex API.

Token storage: ~/.tradingagents/codex_auth.json
"""

import base64
import hashlib
import json
import os
import secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Optional
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

# OAuth constants (from @mariozechner/pi-ai)
CLIENT_ID = "app_EMoamEEZ73f0CkXaXp7hrann"
AUTHORIZE_URL = "https://auth.openai.com/oauth/authorize"
TOKEN_URL = "https://auth.openai.com/oauth/token"
REDIRECT_URI = "http://localhost:1455/auth/callback"
SCOPE = "openid profile email offline_access"

AUTH_STORE_PATH = Path.home() / ".tradingagents" / "codex_auth.json"

_SUCCESS_HTML = b"""<!DOCTYPE html><html><body>
<h2>Authentication successful!</h2>
<p>You can close this window and return to TradingAgents.</p>
</body></html>"""

_ERROR_HTML = b"""<!DOCTYPE html><html><body>
<h2>Authentication failed</h2>
<p>%s</p></body></html>"""


# ── PKCE helpers ────────────────────────────────────────────────────────────

def _generate_pkce() -> tuple[str, str]:
    """Return (verifier, challenge) for PKCE S256."""
    verifier = secrets.token_urlsafe(48)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return verifier, challenge


# ── Token exchange ───────────────────────────────────────────────────────────

def _post_token(body: dict) -> dict:
    data = urlencode(body).encode()
    req = Request(TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read())


def _exchange_code(code: str, verifier: str) -> dict:
    return _post_token({
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": REDIRECT_URI,
    })


def _refresh_token(refresh: str) -> dict:
    return _post_token({
        "grant_type": "refresh_token",
        "refresh_token": refresh,
        "client_id": CLIENT_ID,
    })


# ── JWT helpers ──────────────────────────────────────────────────────────────

def _decode_jwt_payload(token: str) -> Optional[dict]:
    parts = token.split(".")
    if len(parts) != 3:
        return None
    try:
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        return json.loads(base64.urlsafe_b64decode(padded))
    except Exception:
        return None


def _extract_account_id(access_token: str) -> Optional[str]:
    payload = _decode_jwt_payload(access_token)
    if not payload:
        return None
    auth = payload.get("https://api.openai.com/auth", {})
    account_id = auth.get("chatgpt_account_id")
    if isinstance(account_id, str) and account_id:
        return account_id
    return None


def _extract_email(access_token: str) -> Optional[str]:
    payload = _decode_jwt_payload(access_token)
    if not payload:
        return None
    profile = payload.get("https://api.openai.com/profile", {})
    email = profile.get("email")
    return email if isinstance(email, str) and email.strip() else None


# ── Local callback server ────────────────────────────────────────────────────

class _CallbackHandler(BaseHTTPRequestHandler):
    code: Optional[str] = None
    expected_state: str = ""
    event: threading.Event = threading.Event()

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/auth/callback":
            self._respond(404, _ERROR_HTML % b"Not found.")
            return
        params = parse_qs(parsed.query)
        state = params.get("state", [None])[0]
        code = params.get("code", [None])[0]
        if state != self.expected_state:
            self._respond(400, _ERROR_HTML % b"State mismatch.")
            return
        if not code:
            self._respond(400, _ERROR_HTML % b"Missing code.")
            return
        _CallbackHandler.code = code
        _CallbackHandler.event.set()
        self._respond(200, _SUCCESS_HTML)

    def _respond(self, status: int, body: bytes):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass  # suppress server logs


# ── Token store ──────────────────────────────────────────────────────────────

def _load_stored_token() -> Optional[dict]:
    try:
        if AUTH_STORE_PATH.exists():
            return json.loads(AUTH_STORE_PATH.read_text())
    except Exception:
        pass
    return None


def _save_token(data: dict) -> None:
    AUTH_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
    AUTH_STORE_PATH.write_text(json.dumps(data, indent=2))


# ── Public API ───────────────────────────────────────────────────────────────

def login() -> dict:
    """Run the ChatGPT Codex OAuth flow.

    Opens a browser, waits for the callback on localhost:1455, exchanges the
    code for tokens, and saves them to disk.

    Returns a dict with keys: access, refresh, expires, account_id, email.
    """
    verifier, challenge = _generate_pkce()
    state = secrets.token_hex(16)

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
        "id_token_add_organizations": "true",
        "codex_cli_simplified_flow": "true",
        "originator": "tradingagents",
    }
    auth_url = AUTHORIZE_URL + "?" + urlencode(params)

    # Reset handler state
    _CallbackHandler.code = None
    _CallbackHandler.expected_state = state
    _CallbackHandler.event.clear()

    server = HTTPServer(("127.0.0.1", 1455), _CallbackHandler)
    server_thread = threading.Thread(target=server.handle_request, daemon=True)
    server_thread.start()

    print(f"\nOpening browser for ChatGPT authentication...")
    print(f"If the browser does not open, visit:\n  {auth_url}\n")
    webbrowser.open(auth_url)

    # Wait up to 5 minutes
    if not _CallbackHandler.event.wait(timeout=300):
        server.server_close()
        raise TimeoutError("OAuth callback timed out (5 minutes).")

    server.server_close()
    code = _CallbackHandler.code
    if not code:
        raise RuntimeError("No authorization code received.")

    print("Exchanging authorization code for tokens...")
    token_data = _exchange_code(code, verifier)

    access = token_data["access_token"]
    refresh = token_data["refresh_token"]
    expires = int(time.time()) + int(token_data["expires_in"])
    account_id = _extract_account_id(access)
    email = _extract_email(access)

    if not account_id:
        raise RuntimeError("Failed to extract account_id from access token.")

    creds = {
        "access": access,
        "refresh": refresh,
        "expires": expires,
        "account_id": account_id,
        "email": email,
    }
    _save_token(creds)
    print(f"Logged in as: {email or account_id}")
    return creds


def get_valid_token() -> dict:
    """Return a valid (refreshed if needed) token dict.

    If no stored token exists, runs the full OAuth flow.
    Refreshes automatically when the token is within 5 minutes of expiry.

    Returns dict with keys: access, account_id.
    """
    creds = _load_stored_token()
    if not creds:
        creds = login()
        return creds

    expires = creds.get("expires", 0)
    # Refresh if expiring in < 5 minutes
    if expires - time.time() < 300:
        print("Access token expiring soon, refreshing...")
        try:
            token_data = _refresh_token(creds["refresh"])
            creds["access"] = token_data["access_token"]
            creds["refresh"] = token_data["refresh_token"]
            creds["expires"] = int(time.time()) + int(token_data["expires_in"])
            account_id = _extract_account_id(creds["access"])
            if account_id:
                creds["account_id"] = account_id
            _save_token(creds)
        except Exception as e:
            print(f"Token refresh failed: {e}. Re-authenticating...")
            creds = login()

    return creds


def logout() -> None:
    """Remove stored credentials."""
    if AUTH_STORE_PATH.exists():
        AUTH_STORE_PATH.unlink()
        print("Logged out from ChatGPT Codex.")
