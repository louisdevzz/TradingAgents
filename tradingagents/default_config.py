import os

DEFAULT_CONFIG = {
    "project_dir": os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
    "results_dir": os.getenv("TRADINGAGENTS_RESULTS_DIR", "./results"),
    "data_cache_dir": os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), ".")),
        "dataflows/data_cache",
    ),
    # LLM settings
    # Use "openai-codex" for ChatGPT OAuth (no API key needed, browser login).
    # Use "openai" / "anthropic" / "google" / "xai" / "openrouter" / "ollama"
    # to authenticate via the corresponding *_API_KEY environment variable.
    "llm_provider": "openai-codex",
    "deep_think_llm": "gpt-5.4",
    "quick_think_llm": "gpt-5.3-codex",
    "backend_url": None,  # None = use provider default; set to override
    # Provider-specific thinking configuration
    "google_thinking_level": None,      # "high", "minimal", etc.
    "openai_reasoning_effort": None,    # "medium", "high", "low"
    "anthropic_effort": None,           # "high", "medium", "low"
    # Output language for analyst reports and final decision
    # Internal agent debate stays in English for reasoning quality
    "output_language": "English",
    # Debate and discussion settings
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    "max_recur_limit": 100,
    # Data vendor configuration
    # Category-level configuration (default for all tools in category)
    # Options per category: yfinance, alpha_vantage, ssi_iboard (Vietnam stocks)
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
    # Market mode: "global" (Forex/international) or "vietnam" (SSI iBoard)
    "market_mode": "global",
    # Tool-level configuration (takes precedence over category-level)
    "tool_vendors": {
        # Example: "get_stock_data": "alpha_vantage",  # Override category default
    },
}
