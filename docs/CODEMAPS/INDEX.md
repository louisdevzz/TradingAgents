# TradingAgents Codebase Index

**Last Updated:** 2026-04-02  
**Version:** 0.2.3  
**Framework:** Multi-Agent LLM Trading System using LangGraph

## Overview

TradingAgents is a sophisticated multi-agent trading framework that mirrors real-world trading firms. It orchestrates specialized LLM-powered agents to analyze market conditions, conduct debates on investment strategies, manage risk, and execute trading decisions.

## Project Structure

```
TradingAgents/
├── tradingagents/              # Main package
│   ├── agents/                 # Agent implementations
│   │   ├── analysts/           # Analysis agents
│   │   ├── researchers/        # Bullish/bearish researchers
│   │   ├── risk_mgmt/          # Risk debate agents
│   │   ├── managers/           # Portfolio & research managers
│   │   ├── trader/             # Trader agent
│   │   └── utils/              # Shared utilities & tools
│   ├── graph/                  # LangGraph workflow orchestration
│   ├── dataflows/              # Data source interfaces
│   ├── llm_clients/            # Multi-provider LLM support
│   └── default_config.py       # Configuration settings
├── cli/                        # Interactive CLI interface
├── tests/                      # Test suite
└── main.py                     # Example usage
```

## Key Components

### 1. **Agent Architecture** (`tradingagents/agents/`)
- **Analysts**: Market, Technical, Social Media, News, Fundamentals
- **Researchers**: Bull and Bear perspectives
- **Risk Management**: Aggressive, Conservative, Neutral debators
- **Managers**: Research Manager, Portfolio Manager
- **Trader**: Synthesizes analysis into trading decisions

### 2. **Graph Orchestration** (`tradingagents/graph/`)
Core workflow management using LangGraph:
- `trading_graph.py` - Main orchestrator
- `setup.py` - Graph configuration
- `propagation.py` - State propagation
- `conditional_logic.py` - Flow control
- `reflection.py` - Learning from past trades
- `signal_processing.py` - Decision extraction

### 3. **Data Layer** (`tradingagents/dataflows/`)
Multi-source data integration:
- **Stock Data**: yfinance, Alpha Vantage
- **Fundamentals**: Financial statements, ratios
- **Technical**: MACD, RSI, and other indicators
- **News**: Company and market news
- **Sentiment**: Social media analysis

### 4. **LLM Integration** (`tradingagents/llm_clients/`)
Provider abstraction for:
- OpenAI (GPT-5.x models)
- Google (Gemini models)
- Anthropic (Claude models)
- xAI (Grok models)
- OpenRouter, Ollama

## Codemaps by Area

| Document | Coverage | Focus |
|----------|----------|-------|
| [Agents Architecture](./agents.md) | `tradingagents/agents/` | Agent types, responsibilities, tool access |
| [Graph Workflow](./graph.md) | `tradingagents/graph/` | LangGraph setup, state flow, execution |
| [Data Integration](./dataflows.md) | `tradingagents/dataflows/` | Data sources, vendor support, caching |
| [LLM Clients](./llm_clients.md) | `tradingagents/llm_clients/` | Provider support, model configuration |
| [CLI Interface](./cli.md) | `cli/` | Interactive CLI, configuration UI |

## Execution Flow

```
┌─────────────────────────────────────────────────┐
│ 1. Initialize TradingAgentsGraph                │
│    - Load configuration                         │
│    - Create LLM clients (deep + quick)          │
│    - Build agent nodes                          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 2. Analyst Phase (Parallel)                     │
│    ├─ Market Analyst → market_report            │
│    ├─ Technical Analyst → technical insights    │
│    ├─ Social Media Analyst → sentiment_report   │
│    ├─ News Analyst → news_report                │
│    └─ Fundamentals Analyst → fundamentals_report│
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 3. Research Debate Phase (Multi-round)          │
│    ├─ Bull Researcher argues for buy            │
│    ├─ Bear Researcher argues for sell           │
│    ├─ Rounds configured via max_debate_rounds   │
│    └─ Research Manager makes investment_plan    │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 4. Trading Decision Phase                       │
│    └─ Trader synthesizes all reports into plan  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 5. Risk Management Phase (Multi-round)          │
│    ├─ Aggressive Debator (risk appetite high)   │
│    ├─ Conservative Debator (minimize risk)      │
│    ├─ Neutral Debator (balanced view)           │
│    └─ Portfolio Manager approves/rejects        │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│ 6. Decision Output                              │
│    └─ final_trade_decision (BUY/HOLD/SELL)      │
└─────────────────────────────────────────────────┘
```

## State Management

### Core State (AgentState)
```
- company_of_interest: str        # Ticker symbol
- trade_date: str                 # Analysis date
- messages: List[Message]         # LangChain message history
- market_report: str              # Analyst outputs
- sentiment_report: str
- news_report: str
- fundamentals_report: str
- investment_debate_state: InvestDebateState
- investment_plan: str
- trader_investment_plan: str
- risk_debate_state: RiskDebateState
- final_trade_decision: str       # Final output
```

### Memory System
Each agent type maintains persistent memory:
- `bull_memory` - Bullish researcher decisions
- `bear_memory` - Bearish researcher decisions
- `trader_memory` - Trader decisions
- `invest_judge_memory` - Research manager decisions
- `portfolio_manager_memory` - Portfolio manager decisions

## Configuration

Default configuration (`default_config.py`):
- LLM Provider: OpenAI
- Deep Thinking Model: gpt-5.4
- Quick Thinking Model: gpt-5.4-mini
- Debate Rounds: 1
- Risk Discussion Rounds: 1
- Data Vendors: yfinance (configurable per category)

## Entry Points

| Entry Point | Usage | File |
|-----------|-------|------|
| CLI | Interactive configuration & execution | `cli/main.py` |
| Python API | Programmatic usage | `tradingagents/graph/trading_graph.py` |
| Direct Script | Development & testing | `main.py` |

## Key Design Patterns

### 1. **Agent Factory Pattern**
Each agent type has a factory function:
```python
def create_market_analyst(llm) -> callable:
    def market_analyst_node(state): ...
    return market_analyst_node
```

### 2. **Tool Binding**
Agents bind to specific tools for data access:
```python
chain = prompt | llm.bind_tools(tools)
result = chain.invoke(state["messages"])
```

### 3. **Memory Persistence**
Agents maintain memories between trades:
```python
memory = FinancialSituationMemory(agent_name, config)
memory.save_decision(decision, performance)
```

### 4. **Multi-Provider LLM Factory**
Abstract client creation:
```python
client = create_llm_client(provider, model, base_url, **kwargs)
llm = client.get_llm()
```

## Related Documentation

- [README.md](../README.md) - Project overview and installation
- [agents.md](./agents.md) - Detailed agent architecture
- [graph.md](./graph.md) - Graph workflow details
- [dataflows.md](./dataflows.md) - Data source architecture
- [llm_clients.md](./llm_clients.md) - LLM provider support

## Quick Start

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Initialize framework
config = DEFAULT_CONFIG.copy()
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis
final_state, decision = ta.propagate("NVDA", "2026-01-15")

# Process decision
print(decision)  # Output: BUY/HOLD/SELL with reasoning
```

## Dependencies

Key packages:
- **LangChain/LangGraph** - Agentic framework
- **yfinance** - Stock data
- **pandas** - Data manipulation
- **backtrader** - Backtesting
- **questionary** - CLI prompts
- **redis** - Caching
- **typer** - CLI framework

See `pyproject.toml` for full dependency list.

---

**Note**: This documentation reflects the codebase architecture as of v0.2.3. For the latest information, refer to individual module codemaps and the source code.
