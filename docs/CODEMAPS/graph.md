# Graph Workflow Codemap

**Last Updated:** 2026-04-02  
**Directory:** `tradingagents/graph/`  
**Core Framework:** LangGraph StateGraph

## Overview

The graph module orchestrates the entire trading workflow using LangGraph's StateGraph, managing agent execution, state transitions, and conditional routing between different analysis phases.

## Directory Structure

```
graph/
├── __init__.py                  # Module exports
├── trading_graph.py             # Main TradingAgentsGraph class
├── setup.py                     # GraphSetup for workflow construction
├── propagation.py               # Propagator for state initialization
├── conditional_logic.py         # Routing logic between phases
├── reflection.py                # Learning from past trades
└── signal_processing.py         # Decision extraction
```

## Core Components

### 1. TradingAgentsGraph (`trading_graph.py`)

**Main orchestrator class that coordinates all agents and manages execution.**

#### Constructor

```python
class TradingAgentsGraph:
    def __init__(
        self,
        selected_analysts=["market", "social", "news", "fundamentals"],
        debug=False,
        config: Dict[str, Any] = None,
        callbacks: Optional[List] = None,
    ):
```

**Responsibilities:**
1. Initialize LLM clients (deep and quick thinking)
2. Create memory instances for all agents
3. Build tool nodes for data access
4. Instantiate components (GraphSetup, Propagator, etc.)
5. Compile the LangGraph workflow

**Key Attributes:**
- `config` - Configuration dictionary
- `deep_thinking_llm` - LLM for complex reasoning
- `quick_thinking_llm` - LLM for fast tasks
- `bull_memory`, `bear_memory` - Agent memories
- `graph` - Compiled LangGraph StateGraph
- `curr_state` - Current execution state

#### Main Methods

##### propagate(company_name, trade_date)

```python
def propagate(self, company_name, trade_date):
    """Run the trading agents graph for a company on a specific date.
    
    Args:
        company_name: Ticker symbol (e.g., "NVDA")
        trade_date: Analysis date (e.g., "2026-01-15")
    
    Returns:
        (final_state, decision): Full state dict and processed decision
    """
```

**Flow:**
1. Create initial state with company and date
2. Stream/invoke graph execution
3. Store final state for reflection
4. Log results to JSON
5. Process decision signal

##### reflect_and_remember(returns_losses)

```python
def reflect_and_remember(self, returns_losses):
    """Update agent memories based on trade outcomes.
    
    Args:
        returns_losses: Return or loss amount from the trade
    """
```

**Process:**
- Updates bull_memory with outcome
- Updates bear_memory with outcome
- Updates trader_memory with outcome
- Updates manager memories
- Enables future learning

##### process_signal(full_signal)

```python
def process_signal(self, full_signal):
    """Extract core decision from full agent output."""
```

---

### 2. GraphSetup (`setup.py`)

**Constructs the LangGraph StateGraph with all nodes and edges.**

#### Constructor

```python
class GraphSetup:
    def __init__(
        self,
        quick_thinking_llm,
        deep_thinking_llm,
        tool_nodes: Dict[str, ToolNode],
        bull_memory,
        bear_memory,
        trader_memory,
        invest_judge_memory,
        portfolio_manager_memory,
        conditional_logic: ConditionalLogic,
    ):
```

#### setup_graph(selected_analysts)

```python
def setup_graph(self, selected_analysts=["market", "social", "news", "fundamentals"]):
    """Construct and compile the LangGraph workflow.
    
    Creates nodes for:
    1. Selected analyst agents
    2. Research debate agents (bull/bear)
    3. Trader agent
    4. Risk management agents
    
    Creates edges based on conditional logic.
    """
```

**Graph Structure:**

```
START
  ↓
[Parallel Analytics - Selected analysts only]
  ├─ market_analyst → delete_message_market
  ├─ social_analyst → delete_message_social
  ├─ news_analyst → delete_message_news
  └─ fundamentals_analyst → delete_message_fundamentals
  ↓
investment_debate (Research Manager directs to bull/bear)
  ├─ bull_researcher → delete_message_bull
  ├─ bear_researcher → delete_message_bear
  └─ [Conditional: continue debate or move to trader]
  ↓
trader (Trader synthesizes)
  ↓
risk_debate (Portfolio Manager directs to risk agents)
  ├─ aggressive_debator → delete_message_aggressive
  ├─ conservative_debator → delete_message_conservative
  ├─ neutral_debator → delete_message_neutral
  └─ [Conditional: continue debate or complete]
  ↓
END
```

---

### 3. Conditional Logic (`conditional_logic.py`)

**Manages routing decisions throughout the workflow.**

#### ConditionalLogic Class

```python
class ConditionalLogic:
    def __init__(self, max_debate_rounds, max_risk_discuss_rounds):
        self.max_debate_rounds = max_debate_rounds
        self.max_risk_discuss_rounds = max_risk_discuss_rounds
```

#### Key Methods

##### should_continue_invest_debate(state)

```python
def should_continue_invest_debate(self, state: AgentState) -> str:
    """Determine whether to continue research debate or move to trader.
    
    Returns:
        "bull_researcher" | "bear_researcher" | "trader"
    """
```

**Logic:**
- Tracks `investment_debate_state.count`
- Continues debate while count < max_debate_rounds
- Routes to bull/bear alternately
- Moves to trader when debate complete

##### should_continue_risk_discuss(state)

```python
def should_continue_risk_discuss(self, state: AgentState) -> str:
    """Determine whether to continue risk debate or end.
    
    Returns:
        "aggressive_debator" | "conservative_debator" | "neutral_debator" | END
    """
```

**Logic:**
- Tracks `risk_debate_state.count`
- Routes through aggressive → conservative → neutral
- Repeats cycle while count < max_risk_discuss_rounds
- Returns END when complete

---

### 4. Propagator (`propagation.py`)

**Initializes state for graph execution.**

#### Propagator Class

```python
class Propagator:
    def create_initial_state(self, company_name, trade_date) -> AgentState:
        """Create initial state for graph execution.
        
        Returns:
            AgentState with:
            - company_of_interest = company_name
            - trade_date = trade_date
            - messages = []
            - All report fields = ""
            - Debate states initialized
        """
    
    def get_graph_args(self) -> Dict:
        """Get stream/invoke arguments for graph execution."""
```

---

### 5. Reflector (`reflection.py`)

**Processes trade outcomes and updates agent memories.**

#### Reflector Class

```python
class Reflector:
    def __init__(self, llm):
        self.llm = llm  # Quick LLM for reflection summaries
    
    def reflect_bull_researcher(self, state, returns_losses, memory):
        """Analyze bull researcher's decision quality."""
    
    def reflect_bear_researcher(self, state, returns_losses, memory):
        """Analyze bear researcher's decision quality."""
    
    def reflect_trader(self, state, returns_losses, memory):
        """Analyze trader's decision quality."""
    
    def reflect_invest_judge(self, state, returns_losses, memory):
        """Analyze research manager's judgment."""
    
    def reflect_portfolio_manager(self, state, returns_losses, memory):
        """Analyze portfolio manager's decisions."""
```

**Process:**
1. Extracts agent decision from state
2. Compares with actual outcome
3. Generates reflection message
4. Updates agent memory

---

### 6. Signal Processor (`signal_processing.py`)

**Extracts trading decision from agent outputs.**

#### SignalProcessor Class

```python
class SignalProcessor:
    def __init__(self, llm):
        self.llm = llm
    
    def process_signal(self, full_signal: str) -> str:
        """Extract core BUY/HOLD/SELL decision.
        
        Args:
            full_signal: Full final_trade_decision from portfolio manager
        
        Returns:
            Cleaned decision with confidence level and summary
        """
```

**Extracts:**
- Core action (BUY/HOLD/SELL)
- Confidence level
- Key reasons
- Position size recommendation
- Risk metrics

---

## Workflow Execution

### Sequence Diagram

```
User / Script
    │
    ├─ ta = TradingAgentsGraph(config=config)
    │  │ [LLM clients created]
    │  │ [GraphSetup builds graph]
    │  │ [Graph compiled]
    │  └─ returns TradingAgentsGraph instance
    │
    └─ final_state, decision = ta.propagate("NVDA", "2026-01-15")
       │
       ├─ Propagator.create_initial_state()
       │  └─ returns AgentState with empty fields
       │
       ├─ graph.invoke(init_state) or graph.stream(init_state)
       │  │
       │  ├─ [Parallel Analyst Phase]
       │  │  ├─ market_analyst_node()
       │  │  │  ├─ call tool: get_stock_data()
       │  │  │  ├─ call tool: get_indicators()
       │  │  │  ├─ LLM analyzes
       │  │  │  └─ returns market_report
       │  │  │
       │  │  ├─ social_analyst_node()
       │  │  │  ├─ call tool: get_news()
       │  │  │  ├─ LLM analyzes sentiment
       │  │  │  └─ returns sentiment_report
       │  │  │
       │  │  ├─ news_analyst_node()
       │  │  │  ├─ call tools: get_news(), get_global_news()
       │  │  │  ├─ LLM analyzes impact
       │  │  │  └─ returns news_report
       │  │  │
       │  │  └─ fundamentals_analyst_node()
       │  │     ├─ call tools: get_fundamentals(), etc.
       │  │     ├─ LLM analyzes financials
       │  │     └─ returns fundamentals_report
       │  │
       │  ├─ [Sequential Investment Debate Phase]
       │  │  └─ Loop: round 0 to max_debate_rounds
       │  │     ├─ bull_researcher_node()
       │  │     │  ├─ reads: all reports, bear_history
       │  │     │  ├─ LLM generates bull arguments
       │  │     │  └─ appends to bull_history
       │  │     │
       │  │     ├─ bear_researcher_node()
       │  │     │  ├─ reads: all reports, bull_history
       │  │     │  ├─ LLM generates bear arguments
       │  │     │  └─ appends to bear_history
       │  │     │
       │  │     └─ research_manager_node()
       │  │        ├─ reads: bull_history, bear_history
       │  │        ├─ LLM judges debate
       │  │        └─ outputs investment_plan
       │  │
       │  ├─ [Trader Phase]
       │  │  └─ trader_node()
       │  │     ├─ reads: all reports, investment_plan
       │  │     ├─ LLM synthesizes decision
       │  │     └─ outputs trader_investment_plan
       │  │
       │  └─ [Sequential Risk Debate Phase]
       │     └─ Loop: round 0 to max_risk_discuss_rounds
       │        ├─ aggressive_debator_node()
       │        ├─ conservative_debator_node()
       │        ├─ neutral_debator_node()
       │        └─ portfolio_manager_node()
       │           ├─ reads: all risk assessments
       │           ├─ LLM makes final approval
       │           └─ outputs final_trade_decision
       │
       ├─ final_state = result of graph execution
       │
       ├─ _log_state(trade_date, final_state)
       │  └─ saves JSON: eval_results/{ticker}/TradingAgentsStrategy_logs/
       │
       └─ process_signal(final_state["final_trade_decision"])
          └─ returns cleaned decision
```

---

## State Evolution

### Initial State
```python
AgentState(
    company_of_interest="NVDA",
    trade_date="2026-01-15",
    messages=[],
    market_report="",
    sentiment_report="",
    news_report="",
    fundamentals_report="",
    investment_debate_state={
        "bull_history": "",
        "bear_history": "",
        "history": "",
        "current_response": "",
        "judge_decision": "",
        "count": 0,
    },
    investment_plan="",
    trader_investment_plan="",
    risk_debate_state={
        "aggressive_history": "",
        "conservative_history": "",
        "neutral_history": "",
        "history": "",
        "judge_decision": "",
        "count": 0,
    },
    final_trade_decision="",
)
```

### After Analyst Phase
```
market_report = "Technical analysis shows..."
sentiment_report = "Social sentiment indicates..."
news_report = "Company news suggests..."
fundamentals_report = "Financial metrics show..."
messages = [
    HumanMessage("analysis request"),
    AIMessage("market analysis"),
    ToolMessage("stock data"),
    AIMessage("technical conclusions"),
    # ... similar for other analysts
]
```

### After Investment Debate Phase
```
investment_debate_state.bull_history = "Bull says: strong growth potential..."
investment_debate_state.bear_history = "Bear says: valuation concerns..."
investment_debate_state.judge_decision = "Research Manager: BUY on long-term thesis"
investment_plan = "Recommend BUY with position size X..."
messages = [
    # ... all previous messages
    HumanMessage("Bullish perspective..."),
    AIMessage("Bull researcher argument..."),
    HumanMessage("Bearish perspective..."),
    AIMessage("Bear researcher argument..."),
    HumanMessage("Evaluate debate..."),
    AIMessage("Judge's decision..."),
]
```

### After Trader Phase
```
trader_investment_plan = "Buy 100 shares at market, target $500..."
messages = [
    # ... all previous messages
    HumanMessage("Synthesize all insights..."),
    AIMessage("Trader's plan..."),
]
```

### Final State (After Risk Phase)
```
risk_debate_state.aggressive_history = "Aggressive: High risk acceptable..."
risk_debate_state.conservative_history = "Conservative: Reduce position size..."
risk_debate_state.neutral_history = "Neutral: Balanced approach..."
risk_debate_state.judge_decision = "Portfolio Manager: APPROVE 80 shares"
final_trade_decision = "FINAL DECISION: BUY 80 shares with 10% stop loss..."
messages = [
    # ... all previous messages plus risk debate
]
```

---

## Tool Node System

### ToolNode Creation

```python
def _create_tool_nodes(self) -> Dict[str, ToolNode]:
    """Create tool nodes for different data sources."""
    return {
        "market": ToolNode([get_stock_data, get_indicators]),
        "social": ToolNode([get_news]),
        "news": ToolNode([get_news, get_global_news, get_insider_transactions]),
        "fundamentals": ToolNode([
            get_fundamentals,
            get_balance_sheet,
            get_cashflow,
            get_income_statement,
        ]),
    }
```

### Tool Binding

Each agent binds specific tools:
```python
chain = prompt | llm.bind_tools(tools)
result = chain.invoke(state["messages"])
```

When LLM requests a tool call:
1. Tool call is extracted from LLM response
2. ToolNode executes the tool
3. Result is passed back to LLM as ToolMessage
4. LLM processes result and continues

---

## Message Flow

All communication flows through LangChain's message system:

```python
state["messages"] = [
    HumanMessage(content="Analyze this company..."),
    AIMessage(
        content="I'll analyze...",
        tool_calls=[{"name": "get_stock_data", "args": {...}}]
    ),
    ToolMessage(
        name="get_stock_data",
        content="Stock data: price=..., volume=..."
    ),
    AIMessage(content="The stock shows..."),
    # ... continues throughout execution
]
```

---

## Configuration Parameters

From `trading_graph.py`:

```python
self.config = {
    "llm_provider": "openai",           # Provider choice
    "deep_think_llm": "gpt-5.4",       # Complex reasoning
    "quick_think_llm": "gpt-5.4-mini", # Quick tasks
    "max_debate_rounds": 1,             # Investment debate iterations
    "max_risk_discuss_rounds": 1,       # Risk debate iterations
    "backend_url": "https://api.openai.com/v1",  # API endpoint
}
```

---

## Provider-Specific Configuration

```python
def _get_provider_kwargs(self) -> Dict[str, Any]:
    """Get provider-specific LLM configuration."""
    
    # Google: thinking_level = "high" or "minimal"
    # OpenAI: reasoning_effort = "low", "medium", "high"
    # Anthropic: effort = "low", "medium", "high"
```

---

## Logging and Debugging

### Debug Mode

```python
ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("NVDA", "2026-01-15")
```

When debug=True:
- Graph streams results
- Each chunk is pretty-printed
- Full execution trace is captured

### State Logging

```python
def _log_state(self, trade_date, final_state):
    """Log the final state to JSON file."""
    # Creates: eval_results/{ticker}/TradingAgentsStrategy_logs/full_states_log_{date}.json
```

---

## Related Documentation

- [INDEX.md](./INDEX.md) - Project overview
- [agents.md](./agents.md) - Agent details
- [dataflows.md](./dataflows.md) - Data sources

