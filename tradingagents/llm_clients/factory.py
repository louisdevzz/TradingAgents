"""LLM client factory.

Supports two authentication modes:
  1. ChatGPT Codex OAuth (provider="openai-codex") — no API key needed,
     authenticates via browser login to chatgpt.com.
  2. API key from environment (provider="openai" | "anthropic" | "google" |
     "xai" | "openrouter" | "ollama") — reads the key from the corresponding
     env variable.

Only ONE provider is active at a time; set llm_provider in DEFAULT_CONFIG.
"""

from typing import Optional

from .base_client import BaseLLMClient
from .codex_client import CodexClient
from .openai_client import OpenAIClient
from .anthropic_client import AnthropicClient
from .google_client import GoogleClient

# Maps provider id → env variable that holds its API key (None = no key needed)
_PROVIDER_ENV: dict[str, Optional[str]] = {
    "openai": "OPENAI_API_KEY",
    "openai-codex": None,          # OAuth — no env key
    "anthropic": "ANTHROPIC_API_KEY",
    "google": "GOOGLE_API_KEY",
    "xai": "XAI_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "ollama": None,                # local — no key
}

SUPPORTED_PROVIDERS = list(_PROVIDER_ENV.keys())


def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs,
) -> BaseLLMClient:
    """Create an LLM client for the specified provider.

    Args:
        provider: One of the SUPPORTED_PROVIDERS.
            - "openai-codex": ChatGPT OAuth flow (no API key needed).
            - Others: reads API key from the matching environment variable.
        model: Model name/identifier.
        base_url: Optional override for the API endpoint.
        **kwargs: Passed through to the underlying client
            (timeout, max_retries, api_key, reasoning_effort, callbacks, …).

    Returns:
        Configured BaseLLMClient instance.

    Raises:
        ValueError: If provider is not supported.
    """
    p = provider.lower().strip()

    if p not in _PROVIDER_ENV:
        raise ValueError(
            f"Unsupported LLM provider: '{provider}'. "
            f"Choose one of: {', '.join(SUPPORTED_PROVIDERS)}"
        )

    # ── ChatGPT Codex OAuth ──────────────────────────────────────────────────
    if p == "openai-codex":
        return CodexClient(model, base_url, **kwargs)

    # ── API-key providers ────────────────────────────────────────────────────
    if p == "anthropic":
        return AnthropicClient(model, base_url, **kwargs)

    if p == "google":
        return GoogleClient(model, base_url, **kwargs)

    # openai / xai / openrouter / ollama all go through OpenAIClient
    return OpenAIClient(model, base_url, provider=p, **kwargs)
