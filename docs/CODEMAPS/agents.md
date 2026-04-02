# Agents Architecture Codemap

**Last Updated:** 2026-04-02  
**Directory:** `tradingagents/agents/`  
**Framework:** LangChain agents with LangGraph

## Overview

The agents module contains all specialized trading agents that mimic roles in a real trading firm. Each agent is created by a factory function and executes within the LangGraph workflow.

## Agent Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│ Analyst Team (Research Phase)                           │
├─────────────────────────────────────────────────────────┤
│ • Market Analyst (technical patterns, price action)     │
│ • Social Media Analyst (sentiment, social signals)      │
│ • News Analyst (market news, macro events)              │
│ • Fundamentals Analyst (financial metrics, valuations)  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Researcher Team (Debate Phase - Rounds 1 to N)          │
├─────────────────────────────────────────────────────────┤
│ • Bull Researcher (bullish arguments, upside potential) │
│ • Bear Researcher (bearish arguments, risk factors)     │
│ • Research Manager (judges debate, creates plan)        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Trader (Synthesis Phase)                                │
├─────────────────────────────────────────────────────────┤
│ • Trader (combines all insights into trading plan)      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Risk Management Team (Risk Debate Phase - Rounds 1 to M) │
├─────────────────────────────────────────────────────────┤
│ • Aggressive Debator (high risk tolerance view)         │
│ • Conservative Debator (low risk, preservation focus)   │
│ • Neutral Debator (balanced risk assessment)            │
│ • Portfolio Manager (approves/rejects trade)            │
└─────────────────────────────────────────────────────────┘
```

## Directory Structure

```
agents/
├── __init__.py                     # Export agent factories
├── analysts/
│   ├── market_analyst.py           # Technical analysis
│   ├── social_media_analyst.py     # Sentiment analysis
│   ├── news_analyst.py             # News & macro analysis
│   └── fundamentals_analyst.py     # Financial analysis
├── researchers/
│   ├── bull_researcher.py          # Bullish perspective
│   └── bear_researcher.py          # Bearish perspective
├── risk_mgmt/
│   ├── aggressive_debator.py       # High risk appetite
│   ├── conservative_debator.py     # Risk averse
│   └── neutral_debator.py          # Balanced view
├── managers/
│   ├── research_manager.py         # Debate judge
│   └── portfolio_manager.py        # Trade approver
├── trader/
│   └── trader.py                   # Trade synthesizer
└── utils/
    ├── agent_states.py             # TypedDict state definitions
    ├── agent_utils.py              # Shared utilities
    ├── memory.py                   # Persistent memory system
    ├── core_stock_tools.py         # Stock data tools
    ├── technical_indicators_tools.py   # Tech indicators
    ├── fundamental_data_tools.py   # Financial data tools
    └── news_data_tools.py          # News & sentiment tools
```

## Analyst Agents

### Market Analyst (`analysts/market_analyst.py`)

**Purpose:** Technical analysis using price patterns, indicators, and trading signals

**Tools:**
- `get_stock_data` - Historical price, volume
- `get_indicators` - MACD, RSI, Bollinger Bands, etc.

**Output:** `market_report`

**Flow:**
1. Retrieves historical price data
2. Calculates technical indicators
3. Identifies patterns (trends, support/resistance)
4. Generates buy/hold/sell signals
5. Writes comprehensive technical report

**Key Functions:**
```python
def create_market_analyst(llm):
    def market_analyst_node(state) -> Dict[str, Any]:
        # 1. Get stock data and indicators
        # 2. Analyze patterns
        # 3. Generate technical report
        return {"market_report": report, "messages": updated_messages}
    return market_analyst_node
```

---

### Social Media Analyst (`analysts/social_media_analyst.py`)

**Purpose:** Sentiment analysis from social media and public discourse

**Tools:**
- `get_news` - Social media sentiment, mentions

**Output:** `sentiment_report`

**Flow:**
1. Gathers social media data and news sentiment
2. Calculates sentiment scores
3. Identifies trend strength and momentum
4. Analyzes retail vs institutional sentiment
5. Generates sentiment report with actionable insights

---

### News Analyst (`analysts/news_analyst.py`)

**Purpose:** Macro-level news analysis and global event impact assessment

**Tools:**
- `get_news` - Company news, market news
- `get_global_news` - Macroeconomic events
- `get_insider_transactions` - Insider trading signals

**Output:** `news_report`

**Flow:**
1. Retrieves company-specific and market-wide news
2. Analyzes insider transactions
3. Assesses impact of macro events
4. Evaluates news sentiment and reliability
5. Generates news impact report

---

### Fundamentals Analyst (`analysts/fundamentals_analyst.py`)

**Purpose:** Financial statement analysis and valuation assessment

**Tools:**
- `get_fundamentals` - Company metrics, ratios
- `get_balance_sheet` - Assets, liabilities, equity
- `get_cashflow` - Cash generation, burn rates
- `get_income_statement` - Revenue, expenses, profitability

**Output:** `fundamentals_report`

**Flow:**
1. Retrieves comprehensive financial data
2. Analyzes key financial metrics (P/E, PEG, debt ratios)
3. Evaluates cash flow health
4. Assesses growth trajectory
5. Generates fundamental valuation report

---

## Researcher Agents

### Bull Researcher (`researchers/bull_researcher.py`)

**Purpose:** Present the strongest bullish case for investment

**Input:** All analyst reports

**Output:** Bullish arguments, bull_history

**Role in Debate:**
- Advocates for BUY/INCREASE positions
- Highlights upside potential
- Counters bear arguments with positive evidence
- Acknowledges risks but frames them as manageable

**Key Prompt Elements:**
- "Present the bullish thesis with supporting evidence"
- "What is the bull case for this investment?"
- "Respond to bear arguments..."

---

### Bear Researcher (`researchers/bear_researcher.py`)

**Purpose:** Present the strongest bearish case for investment

**Input:** All analyst reports

**Output:** Bearish arguments, bear_history

**Role in Debate:**
- Advocates for SELL/REDUCE positions
- Highlights downside risks
- Counters bull arguments with risk evidence
- Questions valuation and growth assumptions

**Key Prompt Elements:**
- "Present the bearish thesis with supporting evidence"
- "What is the bear case for this investment?"
- "Respond to bull arguments..."

---

## Risk Management Agents

### Aggressive Debator (`risk_mgmt/aggressive_debator.py`)

**Purpose:** Advocate for maximum risk exposure within acceptable bounds

**Input:** Trader investment plan, analyst reports

**Output:** Risk assessment from aggressive perspective

**Role:**
- Supports larger position sizes
- Tolerates higher drawdown limits
- Favors concentrated bets
- Emphasizes opportunity cost of inaction

---

### Conservative Debator (`risk_mgmt/conservative_debator.py`)

**Purpose:** Minimize portfolio risk and preserve capital

**Input:** Trader investment plan, analyst reports

**Output:** Risk assessment from conservative perspective

**Role:**
- Recommends smaller position sizes
- Enforces strict stop losses
- Diversifies across positions
- Emphasizes risk-adjusted returns

---

### Neutral Debator (`risk_mgmt/neutral_debator.py`)

**Purpose:** Balance risk and return from a neutral perspective

**Input:** Trader investment plan, analyst reports

**Output:** Balanced risk assessment

**Role:**
- Synthesizes aggressive and conservative views
- Recommends moderate position sizing
- Applies standard risk management rules
- Evaluates overall portfolio impact

---

## Manager Agents

### Research Manager (`managers/research_manager.py`)

**Purpose:** Judge the debate between bull and bear researchers

**Input:** Bull and bear arguments, analyst reports

**Output:** `investment_plan` (synthesized investment thesis)

**Responsibilities:**
1. Reviews bull researcher's bullish case
2. Reviews bear researcher's bearish case
3. Evaluates quality of arguments
4. Weighs evidence and counterarguments
5. Makes final determination on investment merit
6. Recommends action: BUY, HOLD, or SELL

---

### Portfolio Manager (`managers/portfolio_manager.py`)

**Purpose:** Final approval/rejection of trade proposals

**Input:** Trader investment plan, risk assessments

**Output:** `final_trade_decision` (approved trade or rejection)

**Responsibilities:**
1. Reviews trader's plan and risk assessments
2. Checks position size against limits
3. Evaluates portfolio concentration
4. Approves or rejects with explanation
5. Optionally adjusts position size

---

## Trader Agent (`trader/trader.py`)

**Purpose:** Synthesize all analyst and researcher insights into a concrete trading plan

**Input:**
- Market report
- Sentiment report
- News report
- Fundamentals report
- Investment plan from research debate

**Output:** `trader_investment_plan`

**Responsibilities:**
1. Reads all analyst reports
2. Incorporates research manager's judgment
3. Determines:
   - Action: BUY/HOLD/SELL
   - Quantity: Position size
   - Timing: Immediate or staged entry
   - Exit strategy: Target price, stop loss
4. Writes comprehensive trading plan
5. Justifies all decisions with evidence

---

## Utilities & Tools

### Agent States (`utils/agent_states.py`)

**Core State Definitions:**

```python
class AgentState(MessagesState):
    company_of_interest: str
    trade_date: str
    # Analyst outputs
    market_report: str
    sentiment_report: str
    news_report: str
    fundamentals_report: str
    # Debate states
    investment_debate_state: InvestDebateState
    investment_plan: str
    trader_investment_plan: str
    risk_debate_state: RiskDebateState
    # Final decision
    final_trade_decision: str

class InvestDebateState(TypedDict):
    bull_history: str          # Bull researcher conversation
    bear_history: str          # Bear researcher conversation
    history: str               # Combined debate transcript
    current_response: str      # Latest message
    judge_decision: str        # Research manager judgment
    count: int                 # Round number

class RiskDebateState(TypedDict):
    aggressive_history: str    # Aggressive debator messages
    conservative_history: str  # Conservative debator messages
    neutral_history: str       # Neutral debator messages
    history: str               # Combined risk debate transcript
    judge_decision: str        # Portfolio manager decision
    count: int                 # Round number
```

---

### Agent Utils (`utils/agent_utils.py`)

**Shared Functions:**

```python
def build_instrument_context(ticker: str) -> str:
    """Build context about an instrument for the agent."""

def get_language_instruction() -> str:
    """Get language instruction based on config."""

def get_stock_data(ticker: str, start_date: str, end_date: str):
    """Abstract tool for stock data across vendors."""

def get_indicators(ticker: str, start_date: str, end_date: str):
    """Abstract tool for technical indicators."""

def get_fundamentals(ticker: str) -> Dict:
    """Company financial data and metrics."""

def get_balance_sheet(ticker: str) -> Dict:
    """Balance sheet data."""

def get_cashflow(ticker: str) -> Dict:
    """Cash flow statement."""

def get_income_statement(ticker: str) -> Dict:
    """Income statement data."""

def get_news(ticker: str) -> List[Dict]:
    """Company and market news."""

def get_insider_transactions(ticker: str) -> List[Dict]:
    """Insider trading activity."""

def get_global_news() -> List[Dict]:
    """Global market news."""
```

---

### Memory System (`utils/memory.py`)

**FinancialSituationMemory Class:**

```python
class FinancialSituationMemory:
    def __init__(self, agent_name: str, config: Dict):
        self.agent_name = agent_name
        self.decisions = []  # Historical decisions
        self.performance = []  # Returns/losses

    def save_decision(self, decision: str, analysis: str):
        """Persist decision and reasoning."""

    def get_historical_context(self, limit: int = 10) -> str:
        """Retrieve past decisions for context."""

    def reflect(self, outcome: float):
        """Update memory with trade outcome."""
```

**Purpose:**
- Maintain long-term agent "experience"
- Enable learning from past trades
- Inform future decision-making

---

### Tool Categories

#### Core Stock Tools (`utils/core_stock_tools.py`)
- Historical price data
- Volume analysis
- Price trend calculations

#### Technical Indicators (`utils/technical_indicators_tools.py`)
- MACD (Moving Average Convergence Divergence)
- RSI (Relative Strength Index)
- Bollinger Bands
- Moving averages
- Stochastic oscillator

#### Fundamental Data Tools (`utils/fundamental_data_tools.py`)
- P/E ratio, PEG ratio
- Debt ratios
- ROE, ROA
- Free cash flow
- Growth rates

#### News Data Tools (`utils/news_data_tools.py`)
- Company news
- News sentiment
- Social media sentiment
- Market sentiment indices

---

## Agent Instantiation Pattern

All agents follow this factory pattern:

```python
def create_<agent_type>(llm):
    """Create and return an agent node function."""
    
    def agent_node(state: AgentState) -> Dict[str, Any]:
        # 1. Build context from state
        instrument_context = build_instrument_context(state["company_of_interest"])
        current_date = state["trade_date"]
        
        # 2. Define available tools
        tools = [tool1, tool2, ...]
        
        # 3. Create prompt template with system message
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ])
        
        # 4. Bind tools to LLM
        chain = prompt | llm.bind_tools(tools)
        
        # 5. Invoke and process response
        result = chain.invoke(state["messages"])
        
        # 6. Return updated state
        return {
            "messages": state["messages"] + [result],
            "report_field": extracted_report,
        }
    
    return agent_node
```

---

## Interaction Flow

### Single Analysis Cycle:

```
1. State initialization
   ├─ company_of_interest = "NVDA"
   ├─ trade_date = "2026-01-15"
   └─ messages = []

2. Analyst phase (in parallel)
   ├─ market_analyst() → market_report
   ├─ social_analyst() → sentiment_report
   ├─ news_analyst() → news_report
   └─ fundamentals_analyst() → fundamentals_report

3. Research debate phase (sequential, multiple rounds)
   ├─ Round 1:
   │  ├─ bull_researcher() → bull_history
   │  ├─ bear_researcher() → bear_history
   │  └─ research_manager() → investment_plan
   └─ Repeat if max_debate_rounds > 1

4. Trader phase
   └─ trader() → trader_investment_plan

5. Risk management debate phase (sequential, multiple rounds)
   ├─ Round 1:
   │  ├─ aggressive_debator() → aggressive_history
   │  ├─ conservative_debator() → conservative_history
   │  ├─ neutral_debator() → neutral_history
   │  └─ portfolio_manager() → final_trade_decision
   └─ Repeat if max_risk_discuss_rounds > 1
```

---

## Key Configuration Parameters

From `default_config.py`:

```python
config = {
    "deep_think_llm": "gpt-5.4",              # For complex analysis
    "quick_think_llm": "gpt-5.4-mini",        # For quick tasks
    "max_debate_rounds": 1,                   # Research debate iterations
    "max_risk_discuss_rounds": 1,             # Risk debate iterations
    "output_language": "English",             # Output language setting
}
```

---

## Related Documentation

- [INDEX.md](./INDEX.md) - Overview of all areas
- [graph.md](./graph.md) - Graph orchestration details
- [dataflows.md](./dataflows.md) - Data tool implementations

