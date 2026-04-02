# CLI Interface Codemap

**Last Updated:** 2026-04-02  
**Directory:** `cli/`  
**Purpose:** Interactive command-line interface for TradingAgents

## Overview

The CLI module provides an interactive terminal interface for running TradingAgents without writing code. Users can select stocks, configure analysis parameters, and monitor execution through a rich terminal UI.

## Directory Structure

```
cli/
├── __init__.py                  # Module initialization
├── main.py                      # CLI entry point (Typer app)
├── config.py                    # Configuration UI
├── models.py                    # Data models and schemas
├── utils.py                     # Shared utilities
├── announcements.py             # Version/update info
├── stats_handler.py             # Execution statistics
└── static/                      # Static assets
    └── (CLI assets)
```

---

## Entry Point (`main.py`)

**Main CLI application using Typer framework:**

```python
import typer
from rich.console import Console

app = typer.Typer(
    name="TradingAgents",
    help="Multi-Agents LLM Financial Trading Framework",
)

console = Console()

@app.command()
def main():
    """Interactive CLI for TradingAgents analysis."""
    # 1. Display announcements
    # 2. Get configuration from user
    # 3. Run analysis
    # 4. Display results
```

### Installation & Invocation

**After pip install:**
```bash
tradingagents              # Command works directly
```

**From source:**
```bash
python -m cli.main         # Alternative invocation
```

---

## Configuration UI (`config.py`)

**Interactive configuration prompts using Questionary:**

```python
def get_configuration() -> Dict[str, Any]:
    """Prompt user for all configuration options."""
```

### Configuration Steps

#### 1. Select Ticker

```
? Enter stock ticker(s) (comma-separated, e.g., NVDA,GOOGL):
  → User enters: "NVDA"
```

#### 2. Analysis Date

```
? Select analysis date [YYYY-MM-DD format]:
  → User enters: "2026-01-15"
  → Validates format and validates not in future
```

#### 3. LLM Provider Selection

```
? Choose LLM provider:
  > OpenAI (GPT)
    Google (Gemini)
    Anthropic (Claude)
    xAI (Grok)
    OpenRouter
    Ollama (Local)
```

**Provider-specific configuration:**

**OpenAI:**
```
? Select GPT model:
  > gpt-5.4 (Latest, most capable, highest cost)
    gpt-5.4-mini (Compact, fast, lower cost)
    o3 (Advanced reasoning)
    
? Reasoning effort:
  > low (Faster, cheaper)
    medium (Balanced)
    high (Thorough reasoning, higher cost)
```

**Google:**
```
? Select Gemini model:
  > gemini-3.1-pro (Latest)
    gemini-3.1-flash (Fast)
    gemini-2.0-flash (Previous)

? Thinking level:
  > high (Extended thinking enabled)
    minimal (Fast, no thinking)
```

**Anthropic:**
```
? Select Claude model:
  > claude-4.6 (Latest)
    claude-4.0 (Previous)

? Effort level:
  > high (Extended thinking)
    medium (Balanced)
    low (Fast)
```

#### 4. Research Depth

```
? Maximum debate rounds (1-5):
  Default: 1
  → User enters: "2"
```

This affects:
- Investment debate rounds (bull vs bear)
- Risk debate rounds (aggressive vs conservative)

#### 5. Data Vendor Configuration

```
? Use Alpha Vantage for data (requires API key)?
  > Yes - Use Alpha Vantage (premium data)
    No - Use yfinance (free, no API key needed)
```

**Advanced vendor configuration:**
```
? Configure data vendors:
  Stock APIs: [yfinance / alpha_vantage]
  Technical Indicators: [yfinance / alpha_vantage]
  Fundamental Data: [yfinance / alpha_vantage]
  News Data: [yfinance / alpha_vantage]
```

#### 6. Analyst Selection

```
? Select analysts to include (space to toggle):
  ☑ Market Analyst (technical analysis)
  ☑ Social Media Analyst (sentiment)
  ☑ News Analyst (macro events)
  ☑ Fundamentals Analyst (financial statements)
```

#### 7. Output Language

```
? Output language for reports:
  > English
    Spanish
    French
    German
    Portuguese
    Chinese (Simplified)
    Chinese (Traditional)
    Japanese
    Korean
    Russian
```

**Note:** Internal agent debate remains in English for reasoning quality.

#### 8. Verification & Confirmation

```
Configuration Summary:
  Ticker: NVDA
  Analysis Date: 2026-01-15
  LLM Provider: OpenAI (GPT-5.4)
  Reasoning Effort: high
  Debate Rounds: 2
  Risk Discussion Rounds: 1
  Data Vendor: yfinance
  Analysts: market, social, news, fundamentals
  Output Language: English
  
? Proceed with analysis? [Y/n]
```

---

## Data Models (`models.py`)

**Pydantic models for configuration validation:**

```python
from pydantic import BaseModel, Field, validator

class LLMConfig(BaseModel):
    """LLM configuration."""
    provider: str = Field(
        default="openai",
        description="LLM provider: openai, google, anthropic, xai, openrouter, ollama"
    )
    deep_think_model: str = Field(default="gpt-5.4")
    quick_think_model: str = Field(default="gpt-5.4-mini")
    reasoning_effort: Optional[str] = Field(
        default=None,
        description="OpenAI reasoning effort: low, medium, high"
    )
    thinking_level: Optional[str] = Field(
        default=None,
        description="Google thinking level: high, minimal"
    )
    effort: Optional[str] = Field(
        default=None,
        description="Anthropic effort: low, medium, high"
    )

class DataVendorConfig(BaseModel):
    """Data vendor configuration."""
    core_stock_apis: str = Field(default="yfinance")
    technical_indicators: str = Field(default="yfinance")
    fundamental_data: str = Field(default="yfinance")
    news_data: str = Field(default="yfinance")

class AnalysisConfig(BaseModel):
    """Full analysis configuration."""
    tickers: List[str] = Field(description="Stock ticker symbols")
    analysis_date: str = Field(description="Analysis date YYYY-MM-DD")
    llm_config: LLMConfig
    data_vendor_config: DataVendorConfig
    debate_rounds: int = Field(ge=1, le=5, default=1)
    risk_debate_rounds: int = Field(ge=1, le=5, default=1)
    selected_analysts: List[str] = Field(
        default=["market", "social", "news", "fundamentals"]
    )
    output_language: str = Field(default="English")
    
    @validator("analysis_date")
    def validate_date(cls, v):
        # Validate date format and not in future
        pass
    
    @validator("tickers")
    def validate_tickers(cls, v):
        # Validate ticker format (alphanumeric, length)
        pass
```

---

## Utilities (`utils.py`)

**Shared CLI utilities:**

```python
def validate_ticker(ticker: str) -> bool:
    """Validate ticker format."""
    return bool(re.match(r'^[A-Z0-9]{1,5}$', ticker.upper()))

def validate_date(date_str: str) -> bool:
    """Validate date format and not in future."""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj <= datetime.now()
    except ValueError:
        return False

def format_currency(amount: float) -> str:
    """Format number as currency."""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format as percentage."""
    return f"{value:+.2f}%"

def display_table(data: List[Dict], title: str) -> None:
    """Display formatted table in terminal."""
    # Uses Rich library for formatting
    pass

def display_progress(
    current: int,
    total: int,
    description: str
) -> None:
    """Show progress bar."""
    # Uses Rich progress bar
    pass
```

---

## Announcements (`announcements.py`)

**Display version info and updates:**

```python
def show_version_info():
    """Display TradingAgents version and news."""
    console.print("""
    ╔════════════════════════════════════════════════════════╗
    ║         TradingAgents v0.2.3 - Welcome!                ║
    ║                                                        ║
    ║  Latest Features:                                      ║
    ║  • Multi-language output support                       ║
    ║  • GPT-5.4 family model support                        ║
    ║  • Proxy support for corporate networks                ║
    │  • Improved backtesting date fidelity                  ║
    ╚════════════════════════════════════════════════════════╝
    """)

def check_api_keys(provider: str) -> bool:
    """Check if required API keys are set."""
    required_keys = {
        "openai": "OPENAI_API_KEY",
        "google": "GOOGLE_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "xai": "XAI_API_KEY",
    }
    
    key = required_keys.get(provider)
    if not key or not os.getenv(key):
        return False
    return True
```

---

## Statistics Handler (`stats_handler.py`)

**Track and display execution statistics:**

```python
class StatsHandler:
    """Track analysis execution statistics."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.tokens_used = 0
        self.estimated_cost = 0.0
        self.agents_executed = []
        self.tools_called = 0
    
    def start(self):
        """Start timing."""
        self.start_time = datetime.now()
    
    def end(self):
        """End timing."""
        self.end_time = datetime.now()
    
    def get_duration(self) -> timedelta:
        """Get execution duration."""
        return self.end_time - self.start_time
    
    def add_agent_execution(self, agent_name: str, duration: float):
        """Record agent execution."""
        self.agents_executed.append({
            "name": agent_name,
            "duration": duration,
        })
    
    def display_summary(self):
        """Display execution summary."""
        # Shows:
        # - Total execution time
        # - Per-agent breakdown
        # - Token usage
        # - Estimated cost
        pass
```

---

## Workflow

### Step 1: Initialize CLI

```bash
$ tradingagents
```

**Output:**
```
╔════════════════════════════════════════════════════════╗
║         TradingAgents v0.2.3 - Welcome!                ║
║    Multi-Agents LLM Financial Trading Framework        ║
╚════════════════════════════════════════════════════════╝

[Latest news and features displayed]
```

---

### Step 2: Configuration Phase

```
? Enter stock ticker(s): NVDA
? Analysis date [YYYY-MM-DD]: 2026-01-15
? Choose LLM provider: [OpenAI / Google / Anthropic / xAI / OpenRouter / Ollama]
→ Selected: OpenAI
? Select GPT model: [gpt-5.4 / gpt-5.4-mini / o3]
→ Selected: gpt-5.4
? Reasoning effort [low / medium / high]: high
? Maximum debate rounds (1-5): 2
? Data vendor [yfinance / alpha_vantage]: yfinance
? Select analysts: [Market / Social / News / Fundamentals]
→ All selected
? Output language: English
? Proceed with analysis? [Y/n]: Y
```

---

### Step 3: Execution Phase

**Live progress display:**

```
Analyzing NVDA (2026-01-15)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1/4] 📊 Market Analyst
  ├─ Fetching stock data...                     ✓ 1.2s
  ├─ Calculating indicators...                  ✓ 0.8s
  ├─ Analyzing patterns...                      ✓ 3.5s
  └─ Market Report Generated                    ✓ 5.5s

[2/4] 📰 News Analyst
  ├─ Fetching news data...                      ✓ 0.9s
  ├─ Analyzing sentiment...                     ✓ 2.3s
  └─ News Report Generated                      ✓ 3.2s

[3/4] 😊 Social Media Analyst
  ├─ Analyzing sentiment...                     ✓ 1.8s
  └─ Sentiment Report Generated                 ✓ 1.8s

[4/4] 📈 Fundamentals Analyst
  ├─ Fetching financial data...                 ✓ 1.5s
  ├─ Analyzing ratios...                        ✓ 2.1s
  └─ Fundamentals Report Generated              ✓ 3.6s

Investment Debate (Round 1/2)
  ├─ Bull Researcher argues...                  ⏳ 4.2s
  ├─ Bear Researcher argues...                  ⏳ 3.8s
  └─ Research Manager judges...                 ⏳ 2.1s

Investment Debate (Round 2/2)
  ├─ Bull Researcher rebuttal...                ⏳ 3.9s
  ├─ Bear Researcher rebuttal...                ⏳ 3.5s
  └─ Research Manager final verdict...          ⏳ 2.3s

Trader Synthesis
  └─ Trader creating investment plan...         ⏳ 4.1s

Risk Management Debate
  ├─ Aggressive Debator assessment...           ⏳ 2.7s
  ├─ Conservative Debator assessment...         ⏳ 2.9s
  ├─ Neutral Debator assessment...              ⏳ 2.5s
  └─ Portfolio Manager decision...              ⏳ 1.8s
```

---

### Step 4: Results Display

**Final Decision:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL TRADING DECISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Decision:     🟢 BUY
Confidence:   85%
Action:       Buy 150 shares
Entry:        Market price
Target:       $500
Stop Loss:    $430

Key Rationale:
  ✓ Strong technical momentum (MACD positive, RSI > 60)
  ✓ Positive earnings revisions this quarter
  ✓ Social sentiment improving over past week
  ✓ Fundamentals: P/E of 35 justified by 40% growth

Risks Identified:
  ⚠ Potential pullback if market corrections
  ⚠ Competitive pressure from AMD increasing
  ⚠ Federal AI regulation discussions

Portfolio Impact:
  Current Position: $10,000
  New Investment: $75,000 (150 shares)
  New Total: $85,000
  Concentration: 88% NVDA
  Risk Rating: Moderate-High
```

**Detailed Reports:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANALYST REPORTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 MARKET ANALYSIS

Technical Overview:
  Current Price: $468.50 (as of 2026-01-15)
  52-Week Range: $380 - $520
  200-Day MA: $445.32
  
Indicators:
  MACD: Positive, signal above zero
  RSI (14): 68 (approaching overbought)
  Bollinger Bands: Price in upper band
  Volume: 15% above average

Pattern Analysis:
  NVDA has broken above key resistance at $460
  Support established at $450
  Bullish flag pattern forming

Recommendation: BUY on continued momentum
```

```
📰 NEWS ANALYSIS

Recent Developments:
  • NVIDIA announces new H200 GPU (positive)
  • Q4 earnings beat expectations (positive)
  • Competition from AMD increasing (negative)
  • AI regulation discussions ongoing (mixed)

Sentiment Trend:
  Past 7 days: Improving (+12%)
  Past 30 days: Strongly positive (+35%)
  
Macroeconomic Context:
  AI sector momentum remains strong
  Semiconductor industry tailwinds
  Market sentiment: Risk-on
```

```
😊 SENTIMENT ANALYSIS

Social Media Sentiment:
  Positive mentions: 72%
  Neutral: 18%
  Negative: 10%
  
Trending Topics:
  1. New H200 GPU announcement
  2. Q4 earnings beat
  3. AI infrastructure expansion
  
Influencer Activity:
  15 bullish posts from tech influencers
  2 cautious posts about valuation
```

```
📈 FUNDAMENTALS ANALYSIS

Company: NVIDIA Corporation (NVDA)
Sector: Semiconductors
Market Cap: $2.3T
Price-to-Earnings (P/E): 35.2
Price-to-Book (P/B): 42.1
Dividend Yield: 0.06%

Growth Metrics:
  Revenue Growth (YoY): 38.2%
  EPS Growth (YoY): 42.5%
  Free Cash Flow: $38B

Financial Health:
  Debt-to-Equity: 0.15 (Conservative)
  Current Ratio: 2.3 (Strong)
  ROE: 118% (Exceptional)

Valuation Assessment:
  P/E relative to growth: Fair
  Historical P/E average: 28
  Fair value estimate: $520
  Upside: 11% from current

Assessment: Fairly valued for growth profile
```

---

### Step 5: Execution Summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Analysis Duration:       45 seconds
Total Tokens Used:      ~18,500
Estimated API Cost:     $0.42

Agents Executed:
  ✓ Market Analyst       5.5s
  ✓ News Analyst         3.2s
  ✓ Social Analyst       1.8s
  ✓ Fundamentals Analyst 3.6s
  ✓ Bull Researcher      4.2s + 3.9s
  ✓ Bear Researcher      3.8s + 3.5s
  ✓ Research Manager     2.1s + 2.3s
  ✓ Trader               4.1s
  ✓ Aggressive Debator   2.7s
  ✓ Conservative Debator 2.9s
  ✓ Neutral Debator      2.5s
  ✓ Portfolio Manager    1.8s

Data Sources Used:
  ✓ yfinance (stock data, indicators, news)
  ✓ 4 analyst agents + 3 research agents = 7 LLM calls

Results saved to:
  eval_results/NVDA/TradingAgentsStrategy_logs/full_states_log_2026-01-15.json
```

---

## Advanced Options

### Backtesting

```bash
$ tradingagents backtest --ticker NVDA --from 2025-01-01 --to 2026-01-15
```

Runs analysis for each trading day and compares decisions against actual prices.

### Batch Analysis

```bash
$ tradingagents batch --file tickers.csv --date 2026-01-15
```

Analyzes multiple tickers for the same date.

### Configuration File

```bash
$ tradingagents --config config.yaml
```

Load configuration from YAML file instead of interactive prompts.

---

## Configuration File Format (YAML)

```yaml
tickers:
  - NVDA
  - GOOGL
  - MSFT

analysis_date: "2026-01-15"

llm_config:
  provider: openai
  deep_think_model: gpt-5.4
  quick_think_model: gpt-5.4-mini
  reasoning_effort: high

data_vendor_config:
  core_stock_apis: yfinance
  technical_indicators: yfinance
  fundamental_data: yfinance
  news_data: yfinance

debate_rounds: 2
risk_debate_rounds: 1

selected_analysts:
  - market
  - social
  - news
  - fundamentals

output_language: English
```

---

## Error Handling

### Missing API Keys

```
ERROR: OPENAI_API_KEY not found in environment
  Set your API key: export OPENAI_API_KEY=sk-...
  Or create .env file with: OPENAI_API_KEY=sk-...
  
  Alternatively, use a different provider:
  - Google Gemini (GOOGLE_API_KEY)
  - Anthropic Claude (ANTHROPIC_API_KEY)
  - Ollama (local, no API key needed)
```

### Invalid Ticker

```
ERROR: Invalid ticker "XYZ123"
  Tickers must be 1-5 uppercase alphanumeric characters
  Examples: NVDA, GOOGL, BRK.B (note: dots not supported)
```

### Date Validation

```
ERROR: Analysis date "2026-01-20" is in the future
  Please select a date on or before: 2026-01-15
```

---

## Related Documentation

- [INDEX.md](./INDEX.md) - Project overview
- [agents.md](./agents.md) - Agent implementations
- [graph.md](./graph.md) - Workflow orchestration

