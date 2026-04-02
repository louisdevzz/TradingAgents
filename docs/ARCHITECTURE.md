# TradingAgents Architecture Guide

**Last Updated:** 2026-04-02  
**Version:** 0.2.3  
**Status:** Complete Documentation

## Quick Navigation

| Document | Focus Area | Audience |
|----------|-----------|----------|
| [CODEMAPS/INDEX.md](./CODEMAPS/INDEX.md) | **Start here** - Project overview, entry points, execution flow | Everyone |
| [CODEMAPS/agents.md](./CODEMAPS/agents.md) | Agent types, responsibilities, tool access, memory system | Developers, Researchers |
| [CODEMAPS/graph.md](./CODEMAPS/graph.md) | LangGraph workflow, state management, execution orchestration | Core Developers |
| [CODEMAPS/dataflows.md](./CODEMAPS/dataflows.md) | Data sources, vendor support, caching, tool abstraction | Data Engineers |
| [CODEMAPS/llm_clients.md](./CODEMAPS/llm_clients.md) | LLM integration, provider support, configuration, models | ML Engineers |
| [CODEMAPS/cli.md](./CODEMAPS/cli.md) | Interactive interface, configuration UI, user workflows | End Users, CLI Developers |

---

## System Overview

### What is TradingAgents?

TradingAgents is a sophisticated multi-agent trading framework that orchestrates specialized LLM-powered agents to analyze financial markets and make trading decisions. It mirrors the structure of a real trading firm with:

- **Analysts** gathering and synthesizing market information
- **Researchers** debating investment merits
- **Traders** synthesizing insights into decisions
- **Risk managers** evaluating and approving trades
- **Portfolio managers** making final approvals

### Key Design Principles

1. **Separation of Concerns** - Each agent has a specific role and scope
2. **Debate-Based Decisions** - Multiple perspectives compete and synthesize
3. **Memory & Learning** - Agents learn from past outcomes
4. **Vendor Agnostic Data** - Switch data sources without code changes
5. **Multi-Provider LLMs** - Support for OpenAI, Google, Anthropic, xAI
6. **Extensible Architecture** - Add new agents, data sources, and providers easily

---

## Execution Architecture

### The Trading Workflow

```
1. ANALYST PHASE (Parallel)
   Market Analyst → market_report
   Social Analyst → sentiment_report
   News Analyst → news_report
   Fundamentals Analyst → fundamentals_report

2. INVESTMENT DEBATE PHASE (Sequential, multi-round)
   Bull Researcher + Bear Researcher debate
   Research Manager judges → investment_plan

3. TRADER SYNTHESIS PHASE
   Trader synthesizes all reports → trader_investment_plan

4. RISK MANAGEMENT PHASE (Sequential, multi-round)
   Aggressive/Conservative/Neutral Debators discuss
   Portfolio Manager decides → final_trade_decision
```

### State Flow

All agents operate on a shared `AgentState` that evolves through the workflow:

```python
AgentState {
    company_of_interest: str          # Ticker
    trade_date: str                   # Analysis date
    messages: List[Message]           # Full message history
    
    # Analyst outputs
    market_report: str
    sentiment_report: str
    news_report: str
    fundamentals_report: str
    
    # Debate states
    investment_debate_state: {
        bull_history: str
        bear_history: str
        judge_decision: str
        count: int  # Round counter
    }
    
    # Trader output
    trader_investment_plan: str
    
    # Risk debate state
    risk_debate_state: {
        aggressive_history: str
        conservative_history: str
        neutral_history: str
        judge_decision: str
        count: int
    }
    
    # Final output
    final_trade_decision: str
}
```

---

## Core Modules

### 1. Agents (`tradingagents/agents/`)

**12 specialized agents organized in teams:**

#### Analyst Team
- **Market Analyst** - Technical analysis, price patterns, indicators
- **Social Media Analyst** - Sentiment from social signals
- **News Analyst** - Company and macro news impact
- **Fundamentals Analyst** - Financial metrics and valuations

#### Researcher Team
- **Bull Researcher** - Advocates for buying, highlights upside
- **Bear Researcher** - Advocates against buying, highlights risks
- **Research Manager** - Judges debate, makes investment judgment

#### Trading Team
- **Trader** - Synthesizes all insights into trading plan

#### Risk Management Team
- **Aggressive Debator** - High risk tolerance perspective
- **Conservative Debator** - Risk minimization perspective
- **Neutral Debator** - Balanced risk assessment
- **Portfolio Manager** - Final trade approval

**Factory Pattern:**
```python
def create_market_analyst(llm):
    def market_analyst_node(state):
        # Agent implementation
        return updated_state
    return market_analyst_node
```

**Tool Access:**
Each agent type binds to specific data tools:
```python
tools = [get_stock_data, get_indicators]  # Market analyst
chain = prompt | llm.bind_tools(tools)
result = chain.invoke(state["messages"])
```

### 2. Graph (`tradingagents/graph/`)

**LangGraph-based workflow orchestration:**

- **trading_graph.py** - Main TradingAgentsGraph class, entry point
- **setup.py** - Constructs StateGraph with all nodes and edges
- **conditional_logic.py** - Routes between debate rounds
- **propagation.py** - Initializes state
- **reflection.py** - Updates memories based on outcomes
- **signal_processing.py** - Extracts BUY/HOLD/SELL decision

**Workflow Control:**
- Parallel analyst execution
- Sequential debate rounds (configurable iterations)
- Conditional routing based on round counters
- Message history threading through all agents

### 3. Dataflows (`tradingagents/dataflows/`)

**Vendor-agnostic data integration:**

**Supported Vendors:**
- **yfinance** (free, no API key)
- **Alpha Vantage** (paid, comprehensive)

**Data Categories:**
- Stock prices and volume
- Technical indicators (MACD, RSI, Bollinger Bands)
- Fundamental metrics (P/E, debt ratios, cash flow)
- News and sentiment
- Insider transactions

**Configuration:**
```python
config = {
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
    "tool_vendors": {
        # Tool-level overrides (precedence over category)
    }
}
```

**Caching:**
- Local file-based cache in `dataflows/data_cache/`
- Expires based on data type (intraday vs historical)
- Reduces API calls and costs

### 4. LLM Clients (`tradingagents/llm_clients/`)

**Multi-provider LLM abstraction:**

**Supported Providers:**
- **OpenAI** - GPT-5.4, GPT-5.4-mini, o3 (with reasoning effort)
- **Google** - Gemini 3.1, Gemini 3.1-flash (with thinking levels)
- **Anthropic** - Claude 4.6, Claude 4.0 (with effort control)
- **xAI** - Grok 4.x
- **OpenRouter** - Multi-provider API
- **Ollama** - Local/open-source models

**Factory Pattern:**
```python
client = create_llm_client(
    provider="openai",
    model="gpt-5.4",
    reasoning_effort="high",
    base_url=None,  # Custom endpoint for proxy
)
llm = client.get_llm()
```

**Advanced Features:**
- Extended thinking (OpenAI o3, Claude, Gemini)
- Reasoning effort control
- Proxy support via custom base_url
- SSL certificate customization
- Cost estimation via model_catalog.py

### 5. CLI (`cli/`)

**Interactive terminal interface:**

**Features:**
- Interactive configuration prompts
- Live progress display
- Rich formatted output
- Analyst reports with tables
- Execution statistics
- API key validation
- Date and ticker validation

**Entry Point:**
```bash
tradingagents              # After pip install
python -m cli.main         # From source
```

---

## Key Concepts

### 1. Agent Memory System

Each major agent maintains persistent memory:

```python
memory = FinancialSituationMemory(agent_name, config)
memory.save_decision(decision_text, analysis)
memory.reflect(trade_outcome)  # Updates based on returns
```

**Purpose:** Enable learning from past trades and improved future decisions

### 2. Tool Binding

Agents access data exclusively through LangChain tool binding:

```python
# Define available tools
tools = [get_stock_data, get_indicators, get_fundamentals]

# Create prompt with tool instructions
prompt = ChatPromptTemplate.from_messages([...])

# Bind tools to LLM
chain = prompt | llm.bind_tools(tools)

# Execute - LLM calls tools as needed
result = chain.invoke(state["messages"])
```

### 3. State Threading

All communication flows through message history:

```python
state["messages"] = [
    HumanMessage("Analyze NVDA..."),
    AIMessage("I'll analyze...", tool_calls=[...]),
    ToolMessage("Stock data: ...", name="get_stock_data"),
    AIMessage("Based on the data..."),
    # Continues through all agents
]
```

### 4. Debate Rounds

Research and risk debates can span multiple rounds:

```python
config = {
    "max_debate_rounds": 2,           # Investment debate rounds
    "max_risk_discuss_rounds": 2,     # Risk debate rounds
}
```

Each round:
- Bull/bear researchers present arguments
- Research manager judges
- Debate state accumulates in history
- Conditional logic routes to next participant

---

## Configuration System

### Default Configuration

```python
DEFAULT_CONFIG = {
    # LLM Settings
    "llm_provider": "openai",
    "deep_think_llm": "gpt-5.4",
    "quick_think_llm": "gpt-5.4-mini",
    
    # Provider-Specific Settings
    "openai_reasoning_effort": None,    # "low", "medium", "high"
    "google_thinking_level": None,      # "high", "minimal"
    "anthropic_effort": None,           # "low", "medium", "high"
    
    # Debate Configuration
    "max_debate_rounds": 1,
    "max_risk_discuss_rounds": 1,
    
    # Data Configuration
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
    
    # Output Configuration
    "output_language": "English",
}
```

### Runtime Configuration

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Customize config
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "google"
config["deep_think_llm"] = "gemini-3.1-pro"
config["google_thinking_level"] = "high"
config["max_debate_rounds"] = 2

# Create framework
ta = TradingAgentsGraph(config=config)

# Run analysis
final_state, decision = ta.propagate("NVDA", "2026-01-15")
```

---

## Common Development Tasks

### Adding a New Agent

1. Create `agents/new_agent.py` with factory function
2. Define system prompt and available tools
3. Add to agent imports in `agents/__init__.py`
4. Register in `graph/setup.py`
5. Add to conditional logic routing if needed
6. Update documentation

### Adding a New Data Source

1. Create adapter in `dataflows/new_source.py`
2. Implement interface functions (get_stock_data, etc.)
3. Add vendor to config options
4. Implement caching if needed
5. Update data layer configuration
6. Test fallback mechanism

### Adding LLM Provider Support

1. Create `llm_clients/new_provider_client.py` extending `BaseLLMClient`
2. Implement `get_llm()` method
3. Add to factory in `llm_clients/factory.py`
4. Add models to `llm_clients/model_catalog.py`
5. Add provider validation to `llm_clients/validators.py`
6. Update CLI configuration options

---

## Testing Strategy

### Unit Tests
- Agent individual functionality
- Data source adapters
- LLM client initialization
- Utility functions

### Integration Tests
- Graph workflow end-to-end
- Agent communication via state
- Data flow from source to agent
- LLM client invocation

### E2E Tests
- Full trading analysis execution
- CLI workflow
- Multi-round debates
- Memory persistence and reflection

---

## Performance Optimization

### Model Selection
- **Deep Thinking LLM** - Complex analysis (research, judgment)
- **Quick Thinking LLM** - Simple tasks (report cleanup, formatting)

### Parallel Execution
- All 4 analysts run in parallel (phase 1)
- Data requests cached to avoid redundant calls
- Memory lookups optimized

### Token Management
- Quick model for fast tasks reduces token usage
- Debate rounds are optional (configurable)
- State trimming between phases removes redundant messages

---

## Monitoring & Debugging

### Debug Mode
```python
ta = TradingAgentsGraph(debug=True, config=config)
final_state, decision = ta.propagate("NVDA", "2026-01-15")
```

When enabled:
- Full message history printed
- Execution trace captured
- Agent reasoning visible

### Logging
```
eval_results/{ticker}/TradingAgentsStrategy_logs/
└── full_states_log_{date}.json
```

Contains:
- All analyst reports
- Debate transcripts
- Trading plan
- Final decision
- Risk assessments

### Statistics Tracking
Via LangChain callbacks:
```python
callbacks = [StatsCallback()]
ta = TradingAgentsGraph(callbacks=callbacks, config=config)
```

Tracks:
- Token usage per agent
- API costs
- Execution time
- Tool calls

---

## Deployment Considerations

### Environment Setup
```bash
# Python 3.10+
python --version

# Install dependencies
pip install -e .

# Set API keys
export OPENAI_API_KEY=sk-...
export GOOGLE_API_KEY=...
export ANTHROPIC_API_KEY=sk-ant-...
```

### Configuration for Production
```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["backend_url"] = "https://proxy.corp.com/openai/v1"  # Corporate proxy
config["max_debate_rounds"] = 1  # Faster execution
config["data_vendors"]["core_stock_apis"] = "yfinance"  # Free, no rate limits
```

### Monitoring
- Set up logging to external service
- Track API costs and token usage
- Monitor decision quality vs outcomes
- Implement circuit breaker for failing data sources

---

## Extensibility

### Add Custom Agents
Create new agent factory following existing patterns - see `agents/analysts/market_analyst.py`

### Custom Data Sources
Implement abstract interface in `dataflows/interface.py` - see `dataflows/y_finance.py`

### Custom LLM Providers
Extend `BaseLLMClient` in `llm_clients/base_client.py` - see `llm_clients/openai_client.py`

### Custom Tool Nodes
Add new tools and bind in `graph/trading_graph.py` `_create_tool_nodes()`

---

## Resources

### Code Documentation
- [CODEMAPS/](./CODEMAPS/) - Comprehensive architecture documentation
- Inline docstrings in all Python modules
- Type hints on all function signatures

### External References
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Research Paper](https://arxiv.org/abs/2412.20138)

### Community
- [Discord Server](https://discord.com/invite/hk9PGKShPK)
- [GitHub Issues](https://github.com/TauricResearch/TradingAgents/issues)
- [GitHub Discussions](https://github.com/TauricResearch/TradingAgents/discussions)

---

## Version History

**v0.2.3** (2026-03)
- Multi-language output support
- GPT-5.4 family models
- Unified model catalog
- Backtesting date fidelity
- Proxy support

**v0.2.2** (2026-03)
- GPT-5.4/Gemini 3.1/Claude 4.6 coverage
- Five-tier rating scale
- OpenAI Responses API
- Anthropic effort control
- Cross-platform stability

**v0.2.0** (2026-02)
- Multi-provider LLM support
- Improved system architecture

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](../LICENSE) file.

