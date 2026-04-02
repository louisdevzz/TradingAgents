"""LLM client for ChatGPT Codex (ChatGPT OAuth).

Calls https://chatgpt.com/backend-api/codex/responses (OpenAI Responses API
format) using the OAuth access token from codex_auth.

The endpoint path /codex/responses is resolved by setting:
    base_url = "https://chatgpt.com/backend-api/codex"
so the openai SDK appends /responses automatically.

Required headers (per @mariozechner/pi-ai):
    chatgpt-account-id   — extracted from the JWT access token
    originator           — "pi"
    OpenAI-Beta          — "responses=experimental"
    User-Agent           — "pi (<platform> <release>; <arch>)"

The Codex Responses API requires `instructions` (system prompt) as a top-level
field, not inside `input`. LangChain puts system messages into `input`, so we
override _get_request_payload to extract them.
"""

import platform
from typing import Any, Optional

from langchain_openai import ChatOpenAI

from .base_client import BaseLLMClient, normalize_content
from .codex_auth import get_valid_token

CODEX_BASE_URL = "https://chatgpt.com/backend-api/codex"

_DEFAULT_INSTRUCTIONS = "You are a helpful AI assistant for financial analysis."

CODEX_KNOWN_MODELS = {
    "gpt-5.4",
    "gpt-5.3-codex",
    "gpt-5.2-codex",
    "gpt-5.1-codex",
}


def _user_agent() -> str:
    system = platform.system().lower()
    release = platform.release()
    machine = platform.machine()
    return f"pi ({system} {release}; {machine})"


def _remove_reasoning_items(payload: dict) -> dict:
    """Remove reasoning/summary items from input when store=false.

    When store=false the server doesn't persist reasoning objects, so any
    reference to them by ID (rs_...) in a subsequent turn causes a 404.
    We drop all items whose type is 'reasoning' or whose id starts with 'rs_'.
    """
    input_items = payload.get("input", [])
    filtered = [
        item for item in input_items
        if not (
            isinstance(item, dict) and (
                item.get("type") == "reasoning"
                or str(item.get("id", "")).startswith("rs_")
            )
        )
    ]
    payload["input"] = filtered
    return payload


def _extract_instructions(payload: dict) -> dict:
    """Move system messages from `input` to the top-level `instructions` field.

    The Codex Responses API requires `instructions` to be a non-empty string.
    LangChain puts system messages inside the `input` array; this function
    extracts them and concatenates their text as `instructions`.
    """
    input_items = payload.get("input", [])
    system_texts: list[str] = []
    remaining: list[dict] = []

    for item in input_items:
        if isinstance(item, dict) and item.get("role") == "system":
            content = item.get("content", "")
            if isinstance(content, str):
                system_texts.append(content)
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") in ("text", "input_text"):
                        system_texts.append(block.get("text", ""))
        else:
            remaining.append(item)

    # Build instructions: prefer extracted system text, fall back to default
    instructions = "\n\n".join(t for t in system_texts if t).strip()
    if not instructions:
        instructions = _DEFAULT_INSTRUCTIONS

    payload["instructions"] = instructions
    payload["input"] = remaining
    return payload


class NormalizedCodexChat(ChatOpenAI):
    """ChatOpenAI for chatgpt.com Codex endpoint.

    Overrides payload construction to extract system messages into
    the `instructions` field required by the Codex Responses API.
    """

    def _get_request_payload(self, input_, *, stop=None, **kwargs) -> dict:
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        _extract_instructions(payload)
        _remove_reasoning_items(payload)
        payload["store"] = False
        # Codex requires stream=True — always use streaming path
        payload["stream"] = True
        return payload

    def invoke(self, input, config=None, **kwargs):
        # Codex requires streaming; collect chunks and merge into one message.
        result = None
        for chunk in self.stream(input, config=config, **kwargs):
            result = chunk if result is None else result + chunk
        return normalize_content(result)


class CodexClient(BaseLLMClient):
    """LLM client that authenticates via ChatGPT OAuth (Codex subscription)."""

    def __init__(self, model: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(model, base_url or CODEX_BASE_URL, **kwargs)
        self.provider = "openai-codex"

    def get_llm(self) -> Any:
        self.warn_if_unknown_model()

        creds = get_valid_token()
        access_token = creds["access"]
        account_id = creds.get("account_id", "")

        default_headers = {
            "chatgpt-account-id": account_id,
            "originator": "pi",
            "OpenAI-Beta": "responses=experimental",
            "User-Agent": _user_agent(),
        }

        llm_kwargs: dict = {
            "model": self.model,
            "api_key": access_token,
            "base_url": self.base_url,
            "default_headers": default_headers,
            "use_responses_api": True,
        }

        for key in ("timeout", "max_retries", "reasoning_effort", "callbacks"):
            if key in self.kwargs:
                llm_kwargs[key] = self.kwargs[key]

        return NormalizedCodexChat(**llm_kwargs)

    def validate_model(self) -> bool:
        return self.model in CODEX_KNOWN_MODELS
