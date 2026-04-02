# Data Integration & Dataflows Codemap

**Last Updated:** 2026-04-02  
**Directory:** `tradingagents/dataflows/`  
**Purpose:** Multi-source data abstraction and vendor support

## Overview

The dataflows module provides a vendor-agnostic interface to multiple data sources, enabling seamless switching between data providers (yfinance, Alpha Vantage) without changing agent code.

## Directory Structure

```
dataflows/
├── __init__.py                     # Module exports
├── config.py                       # Configuration management
├── interface.py                    # Abstract data interfaces
├── utils.py                        # Shared utilities
├── # yfinance implementations
├── y_finance.py                    # Core yfinance adapter
├── yfinance_news.py                # News data from yfinance
├── # Alpha Vantage implementations
├── alpha_vantage.py                # Core alpha vantage adapter
├── alpha_vantage_common.py         # Shared alpha vantage logic
├── alpha_vantage_stock.py          # Stock data from alpha vantage
├── alpha_vantage_fundamentals.py   # Fundamentals from alpha vantage
├── alpha_vantage_news.py           # News from alpha vantage
├── alpha_vantage_indicator.py      # Indicators from alpha vantage
├── stockstats_utils.py             # Technical indicator calculations
└── data_cache/                     # Cached responses
```

---

## Core Architecture

### Configuration System (`config.py`)

**Global Configuration Management:**

```python
# Set configuration
set_config(config_dict)

# Get configuration
config = get_config()
```

**Configuration Structure:**

```python
config = {
    "data_vendors": {
        "core_stock_apis": "yfinance",         # Stock prices, volume
        "technical_indicators": "yfinance",    # MACD, RSI, etc.
        "fundamental_data": "yfinance",        # P/E, debt ratios
        "news_data": "yfinance",               # Company news
    },
    "tool_vendors": {
        # Tool-level overrides (precedence over category-level)
        # "get_stock_data": "alpha_vantage",
    },
    "data_cache_dir": "./dataflows/data_cache",
}
```

**Purpose:**
- Centralized vendor configuration
- Per-category vendor selection
- Tool-level overrides
- Data caching directory

---

### Interface System (`interface.py`)

**Abstract interfaces that all vendors must implement:**

```python
def get_stock_data(
    ticker: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Get stock price and volume data."""
    # Returns: {"prices": [...], "volumes": [...], "dates": [...]}

def get_technical_indicators(
    ticker: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Get technical indicators (MACD, RSI, etc.)."""
    # Returns: {"MACD": [...], "RSI": [...], ...}

def get_fundamentals(ticker: str) -> Dict[str, Any]:
    """Get company fundamental metrics."""
    # Returns: {"P/E": X, "PEG": Y, "debt_ratio": Z, ...}

def get_balance_sheet(ticker: str) -> Dict[str, Any]:
    """Get balance sheet data."""
    # Returns: {"assets": X, "liabilities": Y, "equity": Z}

def get_cashflow(ticker: str) -> Dict[str, Any]:
    """Get cash flow statement."""
    # Returns: {"operating_cf": X, "free_cf": Y, ...}

def get_income_statement(ticker: str) -> Dict[str, Any]:
    """Get income statement data."""
    # Returns: {"revenue": X, "net_income": Y, ...}

def get_news(ticker: str) -> List[Dict[str, str]]:
    """Get company and market news."""
    # Returns: [{"headline": "...", "summary": "...", "date": "..."}, ...]

def get_insider_transactions(ticker: str) -> List[Dict]:
    """Get insider trading activity."""
    # Returns: [{"insider": "...", "action": "BUY/SELL", "shares": N}, ...]

def get_global_news() -> List[Dict[str, str]]:
    """Get global market news."""
    # Returns: [{"headline": "...", "source": "...", ...}, ...]
```

---

## Vendor Implementations

### YFinance Adapter (`y_finance.py`)

**yfinance** - Python interface to Yahoo Finance. Free, no API key required.

#### Stock Data (`y_finance.py`)

```python
def get_stock_data_yfinance(ticker, start_date, end_date):
    """
    Fetches historical stock price data from yfinance.
    
    Features:
    - Free, no API key needed
    - Daily, weekly, monthly intervals
    - Handles stock splits, dividends
    - Caches responses locally
    
    Returns:
        {
            "dates": ["2026-01-01", ...],
            "closes": [100.0, ...],
            "opens": [99.5, ...],
            "highs": [101.0, ...],
            "lows": [99.0, ...],
            "volumes": [1000000, ...],
            "ticker": "NVDA"
        }
    """
```

#### Technical Indicators (`y_finance.py`)

**Uses stockstats library for indicator calculation:**

```python
def get_technical_indicators_yfinance(ticker, start_date, end_date):
    """
    Calculate technical indicators from OHLCV data.
    
    Indicators:
    - MACD (Moving Average Convergence Divergence)
      Returns: macd, signal, histogram
    - RSI (Relative Strength Index)
      Returns: 14-period RSI values
    - Bollinger Bands
      Returns: upper, middle, lower bands
    - Moving Averages
      Returns: SMA 20, 50, 200
    
    Implementation:
    1. Get stock data via get_stock_data()
    2. Calculate indicators using stockstats
    3. Return formatted indicator data
    """
```

#### Fundamentals (`y_finance.py`)

```python
def get_fundamentals_yfinance(ticker):
    """
    Fetch company financial metrics.
    
    Data Points:
    - P/E Ratio (Price-to-Earnings)
    - PEG Ratio (Price/Earnings to Growth)
    - P/B Ratio (Price-to-Book)
    - Dividend Yield
    - Beta
    - Market Cap
    - 52-Week High/Low
    - Average Volume
    
    Implementation:
    1. Uses yfinance Ticker info
    2. Extracts key metrics
    3. Returns as dictionary
    """
```

#### Financial Statements (`y_finance.py`)

**Balance Sheet:**
```python
def get_balance_sheet_yfinance(ticker):
    """Returns: {"total_assets", "total_liabilities", "total_equity", ...}"""
```

**Income Statement:**
```python
def get_income_statement_yfinance(ticker):
    """Returns: {"total_revenue", "gross_profit", "net_income", ...}"""
```

**Cash Flow:**
```python
def get_cashflow_yfinance(ticker):
    """Returns: {"operating_cash_flow", "investing_cash_flow", "free_cash_flow", ...}"""
```

#### News (`yfinance_news.py`)

```python
def get_news_yfinance(ticker):
    """
    Fetch recent news about a company.
    
    Returns:
    [
        {
            "title": "NVDA announces new chip",
            "description": "Nvidia has announced...",
            "source": "Yahoo Finance",
            "link": "https://...",
            "published_utc": "2026-01-15T10:30:00Z",
            "sentiment": "positive" | "negative" | "neutral"
        },
        ...
    ]
    """
```

---

### Alpha Vantage Adapter

**Alpha Vantage** - Comprehensive financial data API with free tier.

#### Configuration

Requires `ALPHA_VANTAGE_API_KEY` environment variable.

#### Stock Data (`alpha_vantage_stock.py`)

```python
def get_stock_data_alpha_vantage(ticker, start_date, end_date):
    """
    Fetch from Alpha Vantage TIME_SERIES_DAILY.
    
    Features:
    - 500 requests/day free tier
    - 5, 15, 30, 60 minute intervals available
    - Full historical data
    
    Returns: Same format as yfinance for compatibility
    """
```

#### Technical Indicators (`alpha_vantage_indicator.py`)

Alpha Vantage calculates indicators server-side:

```python
def get_indicators_alpha_vantage(ticker, start_date, end_date):
    """
    Use Alpha Vantage technical indicator endpoints.
    
    Supported Indicators:
    - SMA (Simple Moving Average)
    - EMA (Exponential Moving Average)
    - MACD
    - RSI
    - STOCH (Stochastic)
    - ADX
    - CCI
    - ATR
    - OBV (On Balance Volume)
    - HT_TRENDLINE
    
    Implementation:
    1. Call Alpha Vantage API for each indicator
    2. Parse responses
    3. Consolidate into single dict
    """
```

#### Fundamentals (`alpha_vantage_fundamentals.py`)

```python
def get_fundamentals_alpha_vantage(ticker):
    """
    Use Alpha Vantage OVERVIEW endpoint.
    
    Returns:
    {
        "Symbol": "NVDA",
        "AssetType": "Common Stock",
        "Name": "NVIDIA Corporation",
        "Description": "...",
        "CIK": "...",
        "Exchange": "NASDAQ",
        "Currency": "USD",
        "Country": "USA",
        "Sector": "Technology",
        "Industry": "Semiconductors",
        "Address": "...",
        "FiscalYearEnd": "January",
        "LatestQuarter": "2025-10-31",
        "MarketCapitalization": "...",
        "EBITDA": "...",
        "PERatio": "...",
        "PEGRatio": "...",
        "BookValue": "...",
        "DividendPerShare": "...",
        "DividendYield": "...",
        "EPS": "...",
        "RevenuePerShareTTM": "...",
        "ProfitMargin": "...",
        "OperatingMarginTTM": "...",
        "ReturnOnAssetsANNUAL": "...",
        "ReturnOnEquityANNUAL": "...",
        "RevenueTTM": "...",
        "GrossProfitTTM": "...",
        "DilutedEPSTTM": "...",
        "QuarterlyEarningsGrowthYOY": "...",
        "QuarterlyRevenueGrowthYOY": "...",
        "AnalystTargetPrice": "...",
        "TrailingPE": "...",
        "ForwardPE": "...",
        "PriceToSalesRatioTTM": "...",
        "PriceToBookRatio": "...",
        "EVToRevenue": "...",
        "EVToEBITDA": "...",
        "BetaANNUAL": "...",
        "52WeekHigh": "...",
        "52WeekLow": "...",
        "50DayMovingAverage": "...",
        "200DayMovingAverage": "...",
        "SharesOutstanding": "...",
        "SharesFloat": "...",
        "SharesShort": "...",
        "SharesShortPriorMonth": "...",
        "ShortRatio": "...",
        "ShortPercentOutstanding": "...",
        "ShortPercentFloat": "...",
        "PercentInsiders": "...",
        "PercentInstitutions": "...",
        "ForwardAnnualDividendRate": "...",
        "ForwardAnnualDividendYield": "...",
        "PayoutRatio": "...",
        "DividendDate": "...",
        "ExDividendDate": "...",
        "LastSplitFactor": "...",
        "LastSplitDate": "...",
        "PercentChange52Week": "...",
    }
    """
```

#### News (`alpha_vantage_news.py`)

```python
def get_news_alpha_vantage(ticker):
    """
    Use Alpha Vantage NEWS_SENTIMENT endpoint.
    
    Returns:
    [
        {
            "title": "Article title",
            "url": "https://...",
            "time_published": "20260115T103000Z",
            "authors": ["Author 1", "Author 2"],
            "summary": "Article summary",
            "banner_image": "https://...",
            "source": "Source Name",
            "category": "Technology",
            "topics": ["Earnings", "IPO"],
            "overall_sentiment_score": 0.85,  # -1.0 to 1.0
            "overall_sentiment_label": "STRONG_BUY" | "BUY" | "HOLD" | "SELL" | "STRONG_SELL",
            "ticker_sentiment": [
                {
                    "ticker": "NVDA",
                    "relevance_score": 0.95,
                    "ticker_sentiment_score": 0.85,
                    "ticker_sentiment_label": "STRONG_BUY"
                }
            ]
        },
        ...
    ]
    """
```

---

## Technical Indicator Calculations

### Stockstats Library (`stockstats_utils.py`)

Calculates indicators from OHLCV data:

```python
def calculate_macd(close_prices):
    """
    Moving Average Convergence Divergence
    
    Returns:
    {
        "macd": [values],           # 12 EMA - 26 EMA
        "signal": [values],         # 9 EMA of MACD
        "histogram": [values]       # MACD - Signal
    }
    """

def calculate_rsi(close_prices, period=14):
    """
    Relative Strength Index
    
    Returns: [values]  # 0-100, >70 overbought, <30 oversold
    """

def calculate_bollinger_bands(close_prices, period=20, std_dev=2):
    """
    Bollinger Bands
    
    Returns:
    {
        "upper": [values],   # SMA + (std_dev * stdev)
        "middle": [values],  # SMA
        "lower": [values]    # SMA - (std_dev * stdev)
    }
    """

def calculate_moving_average(close_prices, period):
    """Simple moving average."""
```

---

## Data Caching System

### Cache Location

```
dataflows/
└── data_cache/
    ├── yfinance/
    │   ├── stock_data/
    │   │   └── NVDA_2026-01-01_2026-01-31.json
    │   ├── fundamentals/
    │   │   └── NVDA.json
    │   └── news/
    │       └── NVDA.json
    └── alpha_vantage/
        ├── stock_data/
        │   └── NVDA_daily.json
        ├── indicators/
        │   └── NVDA_MACD.json
        └── news/
            └── NVDA_sentiment.json
```

### Cache Key Strategy

```python
def generate_cache_key(vendor, data_type, ticker, dates):
    """
    Generate consistent cache file key.
    
    Format:
    {vendor}_{data_type}_{ticker}_{start_date}_{end_date}.json
    """
```

### Cache Expiration

- **Intraday data** (fundamentals, news): 24 hours
- **Historical prices**: No expiration (immutable)
- **Cached indicators**: Expires with price data

---

## Vendor Selection Flow

### Configuration Precedence

```
1. Tool-level override
   └─ config["tool_vendors"]["get_stock_data"] = "alpha_vantage"

2. Category-level default
   └─ config["data_vendors"]["core_stock_apis"] = "yfinance"

3. Fallback default
   └─ "yfinance"
```

### Example Resolution

```python
# Config
config["data_vendors"]["core_stock_apis"] = "yfinance"
config["tool_vendors"]["get_stock_data"] = "alpha_vantage"

# Call
result = get_stock_data("NVDA", "2026-01-01", "2026-01-31")

# Resolution
vendor = config["tool_vendors"].get("get_stock_data", None)
if vendor:
    vendor = "alpha_vantage"  # Use tool override
else:
    vendor = config["data_vendors"]["core_stock_apis"]  # Use category default

# Execute
result = get_stock_data_alpha_vantage("NVDA", ...)
```

---

## Error Handling

### Rate Limiting

Alpha Vantage free tier: 5 requests/minute, 500/day

```python
def handle_rate_limit():
    """
    Detect 429 responses and back off.
    Retry with exponential backoff.
    """
```

### Fallback Mechanism

```python
def get_stock_data(ticker, start_date, end_date):
    try:
        vendor = get_configured_vendor("core_stock_apis")
        return call_vendor(vendor, ticker, start_date, end_date)
    except Exception as e:
        # Fall back to yfinance if primary vendor fails
        return get_stock_data_yfinance(ticker, start_date, end_date)
```

### Missing Data Handling

- **Weekends/holidays**: Skip, return available dates
- **Delisted symbols**: Return None with error message
- **Insufficient history**: Return partial data with warning

---

## Shared Utilities (`utils.py`)

```python
def parse_date(date_string):
    """Convert various date formats to standard."""

def cache_request(key, data, vendor):
    """Cache API response to avoid redundant calls."""

def load_from_cache(key):
    """Load cached response if valid."""

def is_cache_valid(cached_date, expiration_hours):
    """Check if cached data is still fresh."""

def format_response(raw_data, format_type):
    """Standardize responses across vendors."""
```

---

## Agent Tool Binding

### Dataflow Integration

In `trading_graph.py`, each analyst binds specific tools:

```python
def _create_tool_nodes(self) -> Dict[str, ToolNode]:
    return {
        "market": ToolNode([
            get_stock_data,        # Core stock API
            get_indicators,        # Technical indicators
        ]),
        "social": ToolNode([
            get_news,              # Sentiment/social
        ]),
        "news": ToolNode([
            get_news,              # Company news
            get_global_news,       # Market news
            get_insider_transactions,
        ]),
        "fundamentals": ToolNode([
            get_fundamentals,
            get_balance_sheet,
            get_cashflow,
            get_income_statement,
        ]),
    }
```

---

## Configuration Example

```python
config = {
    "data_vendors": {
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance",
    },
    "tool_vendors": {
        # "get_stock_data": "alpha_vantage",  # Override specific tool
    },
    "data_cache_dir": "./dataflows/data_cache",
}

ta = TradingAgentsGraph(config=config)
```

---

## Related Documentation

- [INDEX.md](./INDEX.md) - Project overview
- [agents.md](./agents.md) - Agent implementations
- [graph.md](./graph.md) - Workflow orchestration

