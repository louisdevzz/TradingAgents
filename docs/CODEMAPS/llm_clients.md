# LLM Clients Integration Codemap

**Last Updated:** 2026-04-02  
**Directory:** `tradingagents/llm_clients/`  
**Purpose:** Multi-provider LLM abstraction and configuration

## Overview

The llm_clients module provides a unified interface for integrating multiple LLM providers with provider-specific configuration for advanced features like extended thinking and reasoning effort control.

## Directory Structure

```
llm_clients/
├── __init__.py                  # Module exports
├── base_client.py               # Abstract base class
├── factory.py                   # Client factory pattern
├── openai_client.py             # OpenAI (GPT) implementation
├── anthropic_client.py          # Anthropic (Claude) implementation
├── google_client.py             # Google (Gemini) implementation
├── model_catalog.py             # Supported models registry
└── validators.py                # Input validation
```

---

## Core Architecture

### Base Client (`base_client.py`)

**Abstract base class defining the interface all clients must implement:**

```python
class BaseLLMClient(ABC):
    """Abstract base for LLM client implementations."""
    
    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """Initialize LLM client.
        
        Args:
            model: Model identifier (e.g., "gpt-5.4")
            base_url: Optional custom API endpoint
            **kwargs: Provider-specific configuration
        """
        self.model = model
        self.base_url = base_url
        self.kwargs = kwargs
    
    @abstractmethod
    def get_llm(self) -> Any:
        """Get configured LangChain LLM instance.
        
        Returns:
            LangChain language model ready for tool binding and invocation
        """
        pass
```

**Responsibilities:**
1. Validate model name
2. Configure API client
3. Apply provider-specific settings
4. Return LangChain-compatible LLM

---

### Factory Pattern (`factory.py`)

**Creates appropriate client based on provider:**

```python
def create_llm_client(
    provider: str,
    model: str,
    base_url: Optional[str] = None,
    **kwargs,
) -> BaseLLMClient:
    """Create LLM client for the specified provider.
    
    Args:
        provider: One of "openai", "anthropic", "google", "xai", "openrouter", "ollama"
        model: Model identifier
        base_url: Optional custom API endpoint (for proxy, local LLM, etc.)
        **kwargs: Provider-specific arguments:
            - http_client: Custom httpx.Client for SSL/proxy
            - http_async_client: Custom httpx.AsyncClient
            - timeout: Request timeout in seconds
            - max_retries: Maximum retry attempts
            - api_key: API key (alternative to env var)
            - callbacks: LangChain callbacks for stats tracking
            - reasoning_effort: OpenAI reasoning effort level
            - thinking_level: Google thinking level
            - effort: Anthropic effort level
    
    Returns:
        Configured BaseLLMClient instance
    
    Raises:
        ValueError: If provider not supported
    """
```

**Provider Mapping:**
```
"openai"     → OpenAIClient(provider="openai")
"ollama"     → OpenAIClient(provider="ollama")
"openrouter" → OpenAIClient(provider="openrouter")
"xai"        → OpenAIClient(provider="xai")
"anthropic"  → AnthropicClient
"google"     → GoogleClient
```

---

## Provider Implementations

### OpenAI Client (`openai_client.py`)

**Supports OpenAI, xAI (Grok), OpenRouter, Ollama**

#### Configuration

```python
class OpenAIClient(BaseLLMClient):
    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        provider: str = "openai",
        **kwargs,
    ):
        """
        Args:
            model: "gpt-5.4", "gpt-5.4-mini", etc.
            base_url: Custom API endpoint
            provider: "openai" | "xai" | "openrouter" | "ollama"
            reasoning_effort: "low" | "medium" | "high" (for o1, o3 models)
            http_client: Custom httpx.Client
            callbacks: LangChain callbacks
        """
```

#### Models

**Latest Models:**
- `gpt-5.4` - Latest flagship model
- `gpt-5.4-mini` - Compact, fast model
- `gpt-4-turbo` - Legacy model
- `gpt-4` - Older model

**Advanced Reasoning Models:**
- `o1` - Specialized reasoning
- `o3` - Enhanced reasoning (new)

#### Reasoning Effort (OpenAI)

```python
# Configuration in default_config.py
config = {
    "openai_reasoning_effort": "medium",  # "low", "medium", "high"
}

# Automatic application
def get_llm(self):
    return ChatOpenAI(
        model=self.model,
        reasoning_effort=self.kwargs.get("reasoning_effort"),
        # Additional config...
    )
```

**Effect:**
- `"low"` - Minimal thinking, faster responses, lower cost
- `"medium"` - Balanced reasoning and performance
- `"high"` - Extended thinking, thorough analysis, higher cost

#### Example Usage

```python
from tradingagents.llm_clients import create_llm_client

# Standard GPT-5.4
client = create_llm_client("openai", "gpt-5.4")
llm = client.get_llm()

# With reasoning effort
client = create_llm_client(
    "openai",
    "gpt-5.4",
    reasoning_effort="high"
)
llm = client.get_llm()

# With proxy/custom endpoint
client = create_llm_client(
    "openai",
    "gpt-5.4",
    base_url="https://proxy.example.com/v1"
)
llm = client.get_llm()

# Ollama (local LLM)
client = create_llm_client(
    "ollama",
    "llama2",
    base_url="http://localhost:11434/v1"
)
llm = client.get_llm()
```

---

### Anthropic Client (`anthropic_client.py`)

**Supports Claude models**

#### Configuration

```python
class AnthropicClient(BaseLLMClient):
    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            model: "claude-4.6", "claude-4.0", etc.
            base_url: Custom API endpoint
            effort: "low" | "medium" | "high"
            http_client: Custom httpx.Client
            callbacks: LangChain callbacks
        """
```

#### Models

**Latest Models:**
- `claude-4.6` - Latest flagship
- `claude-4.0` - Slightly older
- `claude-3.5-sonnet` - Mid-tier

#### Effort Control (Anthropic)

```python
# Configuration in default_config.py
config = {
    "anthropic_effort": "high",  # "low", "medium", "high"
}

# Automatic application
def get_llm(self):
    return ChatAnthropic(
        model=self.model,
        thinking_type="enabled",  # Extended thinking
        budget_tokens=10000,       # Thinking budget
        # Additional config...
    )
```

**Effect:**
- `"low"` - No extended thinking, faster
- `"medium"` - Limited extended thinking
- `"high"` - Full extended thinking enabled

#### Example Usage

```python
from tradingagents.llm_clients import create_llm_client

# Standard Claude
client = create_llm_client("anthropic", "claude-4.6")
llm = client.get_llm()

# With effort control
client = create_llm_client(
    "anthropic",
    "claude-4.6",
    effort="high"
)
llm = client.get_llm()
```

---

### Google Client (`google_client.py`)

**Supports Google Gemini models**

#### Configuration

```python
class GoogleClient(BaseLLMClient):
    def __init__(
        self,
        model: str,
        base_url: Optional[str] = None,
        **kwargs,
    ):
        """
        Args:
            model: "gemini-3.1-pro", "gemini-2.0-flash", etc.
            base_url: Custom API endpoint
            thinking_level: "high" | "minimal"
            http_client: Custom httpx.Client
            callbacks: LangChain callbacks
        """
```

#### Models

**Latest Models:**
- `gemini-3.1-pro` - Latest flagship
- `gemini-3.1-flash` - Compact, fast
- `gemini-2.0-flash` - Previous generation

#### Thinking Level (Google)

```python
# Configuration in default_config.py
config = {
    "google_thinking_level": "high",  # "high", "minimal", None
}

# Automatic application
def get_llm(self):
    return ChatGoogleGenerativeAI(
        model=self.model,
        thinking_config=ThinkingConfig(
            type="ENABLED",
            budget_tokens=10000,
        ) if self.kwargs.get("thinking_level") == "high" else None,
        # Additional config...
    )
```

**Effect:**
- `"high"` - Extended thinking enabled
- `"minimal"` - No extended thinking, faster
- `None` - Default behavior

#### Example Usage

```python
from tradingagents.llm_clients import create_llm_client

# Standard Gemini
client = create_llm_client("google", "gemini-3.1-pro")
llm = client.get_llm()

# With thinking enabled
client = create_llm_client(
    "google",
    "gemini-3.1-pro",
    thinking_level="high"
)
llm = client.get_llm()
```

---

## Model Catalog (`model_catalog.py`)

**Registry of supported models with metadata:**

```python
MODEL_CATALOG = {
    "openai": {
        "gpt-5.4": {
            "display_name": "GPT-5.4 (Latest)",
            "context_window": 128000,
            "cost_per_1m_input_tokens": 2.50,
            "cost_per_1m_output_tokens": 10.00,
            "supports_reasoning_effort": True,
            "supports_extended_thinking": True,
            "max_thinking_tokens": 65000,
            "release_date": "2025-Q4",
        },
        "gpt-5.4-mini": {
            "display_name": "GPT-5.4 Mini",
            "context_window": 128000,
            "cost_per_1m_input_tokens": 0.15,
            "cost_per_1m_output_tokens": 0.60,
            "supports_reasoning_effort": False,
            "supports_extended_thinking": False,
            "release_date": "2025-Q4",
        },
        "o3": {
            "display_name": "O3 (Advanced Reasoning)",
            "context_window": 200000,
            "supports_reasoning_effort": True,
            "supports_extended_thinking": True,
            "max_thinking_tokens": 131072,
            "release_date": "2026-Q1",
        },
    },
    "anthropic": {
        "claude-4.6": {
            "display_name": "Claude 4.6 (Latest)",
            "context_window": 200000,
            "supports_extended_thinking": True,
            "max_thinking_tokens": 10000,
            "release_date": "2025-Q4",
        },
    },
    "google": {
        "gemini-3.1-pro": {
            "display_name": "Gemini 3.1 Pro",
            "context_window": 1000000,
            "supports_thinking": True,
            "max_thinking_tokens": 10000,
            "release_date": "2025-Q4",
        },
    },
}
```

**Provides:**
- Model display names
- Context window sizes
- Cost estimates
- Capability flags
- Release dates

---

## Validators (`validators.py`)

**Input validation for model configuration:**

```python
def validate_model_name(provider: str, model: str) -> bool:
    """Check if model is supported by provider."""
    return model in MODEL_CATALOG.get(provider, {})

def validate_reasoning_effort(value: Optional[str]) -> bool:
    """Check if reasoning effort is valid."""
    return value is None or value in ["low", "medium", "high"]

def validate_thinking_level(value: Optional[str]) -> bool:
    """Check if thinking level is valid."""
    return value is None or value in ["high", "minimal"]

def validate_effort(value: Optional[str]) -> bool:
    """Check if Anthropic effort is valid."""
    return value is None or value in ["low", "medium", "high"]
```

---

## Integration with TradingAgentsGraph

### Initialization

```python
class TradingAgentsGraph:
    def __init__(self, config=None, **kwargs):
        self.config = config or DEFAULT_CONFIG
        
        # Get provider-specific kwargs
        llm_kwargs = self._get_provider_kwargs()
        
        # Create clients
        deep_client = create_llm_client(
            provider=self.config["llm_provider"],
            model=self.config["deep_think_llm"],
            base_url=self.config.get("backend_url"),
            **llm_kwargs,  # Reasoning/thinking config
        )
        quick_client = create_llm_client(
            provider=self.config["llm_provider"],
            model=self.config["quick_think_llm"],
            **llm_kwargs,
        )
        
        self.deep_thinking_llm = deep_client.get_llm()
        self.quick_thinking_llm = quick_client.get_llm()

    def _get_provider_kwargs(self) -> Dict[str, Any]:
        """Build provider-specific kwargs from config."""
        kwargs = {}
        provider = self.config.get("llm_provider", "").lower()
        
        if provider == "google":
            if self.config.get("google_thinking_level"):
                kwargs["thinking_level"] = self.config["google_thinking_level"]
        
        elif provider == "openai":
            if self.config.get("openai_reasoning_effort"):
                kwargs["reasoning_effort"] = self.config["openai_reasoning_effort"]
        
        elif provider == "anthropic":
            if self.config.get("anthropic_effort"):
                kwargs["effort"] = self.config["anthropic_effort"]
        
        return kwargs
```

### Agent Creation

```python
# Analysts use quick_thinking_llm (fast tasks)
analyst = create_market_analyst(self.quick_thinking_llm)

# Complex reasoning uses deep_thinking_llm (if configured with reasoning)
researcher = create_bull_researcher(self.deep_thinking_llm)
```

---

## Configuration Examples

### Standard Configuration

```python
config = {
    "llm_provider": "openai",
    "deep_think_llm": "gpt-5.4",
    "quick_think_llm": "gpt-5.4-mini",
    "backend_url": "https://api.openai.com/v1",
    "openai_reasoning_effort": None,  # No extended thinking by default
}

ta = TradingAgentsGraph(config=config)
```

### With Extended Thinking (OpenAI)

```python
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "o3"  # Advanced reasoning model
config["openai_reasoning_effort"] = "high"
config["max_debate_rounds"] = 2  # Leverage better reasoning

ta = TradingAgentsGraph(config=config)
```

### With Google Gemini

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "google"
config["deep_think_llm"] = "gemini-3.1-pro"
config["quick_think_llm"] = "gemini-3.1-flash"
config["google_thinking_level"] = "high"

ta = TradingAgentsGraph(config=config)
```

### With Claude

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "anthropic"
config["deep_think_llm"] = "claude-4.6"
config["quick_think_llm"] = "claude-4.6"
config["anthropic_effort"] = "high"

ta = TradingAgentsGraph(config=config)
```

### With Local Ollama

```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["deep_think_llm"] = "llama2"
config["quick_think_llm"] = "llama2"
config["backend_url"] = "http://localhost:11434/v1"

ta = TradingAgentsGraph(config=config)
```

### With Proxy/Custom Endpoint

```python
config = DEFAULT_CONFIG.copy()
config["backend_url"] = "https://proxy.corp.com/openai/v1"

ta = TradingAgentsGraph(config=config)
```

---

## API Key Management

### Environment Variables

```bash
# OpenAI
export OPENAI_API_KEY=sk-...

# Google
export GOOGLE_API_KEY=...

# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# xAI
export XAI_API_KEY=...

# OpenRouter
export OPENROUTER_API_KEY=...

# Alpha Vantage (for data, not LLM)
export ALPHA_VANTAGE_API_KEY=...
```

### .env File

```bash
# Copy .env.example to .env and fill in your keys
cp .env.example .env

OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
XAI_API_KEY=...
OPENROUTER_API_KEY=...
ALPHA_VANTAGE_API_KEY=...
```

### Loading in Code

```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in environment")
```

---

## Advanced Features

### Callbacks for Stats Tracking

```python
from langchain.callbacks import BaseCallbackHandler

class StatsCallback(BaseCallbackHandler):
    def __init__(self):
        self.total_tokens = 0
        self.total_cost = 0
    
    def on_llm_end(self, response, **kwargs):
        # Track token usage and costs
        pass

callbacks = [StatsCallback()]
client = create_llm_client(
    "openai",
    "gpt-5.4",
    callbacks=callbacks
)
```

### Custom HTTP Client (SSL/Proxy)

```python
import httpx

# SSL certificate verification disabled
http_client = httpx.Client(verify=False)

client = create_llm_client(
    "openai",
    "gpt-5.4",
    http_client=http_client
)
```

---

## Cost Estimation

Using model catalog:

```python
from tradingagents.llm_clients.model_catalog import MODEL_CATALOG

def estimate_cost(provider, model, input_tokens, output_tokens):
    """Estimate API costs for a request."""
    model_info = MODEL_CATALOG[provider][model]
    input_cost = (input_tokens / 1_000_000) * model_info["cost_per_1m_input_tokens"]
    output_cost = (output_tokens / 1_000_000) * model_info["cost_per_1m_output_tokens"]
    return input_cost + output_cost

# GPT-5.4: 1M input tokens, 500K output tokens
cost = estimate_cost("openai", "gpt-5.4", 1_000_000, 500_000)
print(f"Estimated cost: ${cost:.2f}")
```

---

## Related Documentation

- [INDEX.md](./INDEX.md) - Project overview
- [agents.md](./agents.md) - Agent implementations
- [graph.md](./graph.md) - Workflow orchestration

