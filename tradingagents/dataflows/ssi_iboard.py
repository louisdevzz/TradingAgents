"""SSI iBoard data provider for Vietnam stock market.

Uses the two confirmed working endpoints:
  - GET /stock/{symbol}?boardId=MAIN    → realtime quote, order book, fundamentals
  - GET /le-table/stock/{symbol}?pageSize=N  → intraday tick transactions (max ~100)

Note: SSI iBoard does not expose a historical multi-day OHLCV endpoint via these
paths.  get_stock_data therefore returns today's intraday tick series plus a
current snapshot — sufficient for intraday market analysis.
"""

from __future__ import annotations

from typing import Annotated

import pandas as pd

from .ssi_iboard_common import ssi_get
from .x_tweet_fetcher import build_x_tweet_news_block


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _vnd(value) -> str:
    """Format a VND integer value with thousand separators."""
    try:
        return f"{int(value):,} VND"
    except (TypeError, ValueError):
        return str(value)


def _pct(value) -> str:
    try:
        return f"{float(value):+.2f}%"
    except (TypeError, ValueError):
        return str(value)


def _fetch_quote(symbol: str) -> dict:
    """Fetch realtime quote for a stock."""
    data = ssi_get(f"/stock/{symbol}?boardId=MAIN")
    if data.get("code") != "SUCCESS":
        raise ValueError(f"SSI iBoard returned error for {symbol}: {data.get('message')}")
    return data.get("data", {})


def _fetch_ticks(symbol: str, page_size: int = 100) -> list[dict]:
    """Fetch recent intraday tick transactions (newest first, max ~100)."""
    data = ssi_get(f"/le-table/stock/{symbol}", params={"pageSize": page_size})
    if data.get("code") != "SUCCESS":
        return []
    return (data.get("data") or {}).get("items", [])


# ---------------------------------------------------------------------------
# Public interface – matches VENDOR_METHODS signatures
# ---------------------------------------------------------------------------

def get_stock_data(
    symbol: Annotated[str, "Vietnam stock ticker (e.g. ACB, VNM, VIC)"],
    start_date: Annotated[str, "Start date YYYY-MM-DD (used as context only)"],
    end_date: Annotated[str, "End date YYYY-MM-DD (used as context only)"],
) -> str:
    """Fetch intraday price data for a Vietnam-listed stock from SSI iBoard.

    Returns today's tick-by-tick transactions plus a current session snapshot.
    SSI iBoard does not provide multi-day historical OHLCV via public endpoints.
    """
    symbol_upper = symbol.upper()
    try:
        quote = _fetch_quote(symbol_upper)
        ticks = _fetch_ticks(symbol_upper, page_size=100)
    except Exception as exc:
        return f"Error fetching SSI iBoard data for '{symbol}': {exc}"

    trading_date = quote.get("tradingDate", "")
    if len(trading_date) == 8:  # YYYYMMDD
        trading_date = f"{trading_date[:4]}-{trading_date[4:6]}-{trading_date[6:]}"

    # Build session OHLCV from tick data (ticks are newest-first)
    prices = [t["price"] for t in ticks if t.get("price")]
    open_p = quote.get("openPrice") or (prices[-1] if prices else None)
    high_p = quote.get("highest") or (max(prices) if prices else None)
    low_p = quote.get("lowest") or (min(prices) if prices else None)
    close_p = quote.get("matchedPrice") or (prices[0] if prices else None)
    volume = quote.get("nmTotalTradedQty") or quote.get("stockVol", 0)
    ref_price = quote.get("refPrice") or quote.get("priorClosePrice", 0)

    lines = [
        f"# Vietnam Stock Data: {symbol_upper} (SSI iBoard)",
        f"# Trading Date: {trading_date}",
        f"# Exchange: {quote.get('exchange', '').upper()} | Market: {quote.get('market', '')}",
        f"# Company: {quote.get('companyNameEn', '')} / {quote.get('companyNameVi', '')}",
        "",
        "## Session Summary (Today)",
        f"Reference Price: {_vnd(ref_price)}",
        f"Open: {_vnd(open_p)}",
        f"High: {_vnd(high_p)}",
        f"Low: {_vnd(low_p)}",
        f"Close/Last: {_vnd(close_p)}",
        f"Volume: {int(volume):,} shares",
        f"Value: {_vnd(quote.get('nmTotalTradedValue', 0))}",
        f"Change: {_vnd(quote.get('priceChange', 0))} ({_pct(quote.get('priceChangePercent', 0))})",
        f"Ceiling: {_vnd(quote.get('ceiling', 0))}  |  Floor: {_vnd(quote.get('floor', 0))}",
        "",
        "## Order Book (Top 3 Bid/Ask)",
        f"  Bid 1: {_vnd(quote.get('best1Bid'))} x {quote.get('best1BidVol', 0):,}  |  Ask 1: {_vnd(quote.get('best1Offer'))} x {quote.get('best1OfferVol', 0):,}",
        f"  Bid 2: {_vnd(quote.get('best2Bid'))} x {quote.get('best2BidVol', 0):,}  |  Ask 2: {_vnd(quote.get('best2Offer'))} x {quote.get('best2OfferVol', 0):,}",
        f"  Bid 3: {_vnd(quote.get('best3Bid'))} x {quote.get('best3BidVol', 0):,}  |  Ask 3: {_vnd(quote.get('best3Offer'))} x {quote.get('best3OfferVol', 0):,}",
        "",
        "## Foreign Trading",
        f"  Buy: {int(quote.get('buyForeignQtty', 0)):,} shares ({_vnd(quote.get('buyForeignValue', 0))})",
        f"  Sell: {int(quote.get('sellForeignQtty', 0)):,} shares ({_vnd(quote.get('sellForeignValue', 0))})",
        f"  Remaining foreign room: {int(quote.get('remainForeignQtty', 0)):,} shares",
        "",
    ]

    # Tick table (most recent 30 transactions)
    if ticks:
        lines.append("## Recent Transactions (newest first)")
        lines.append(f"{'Time':>10}  {'Price':>10}  {'Vol':>10}  {'Side':>4}  {'Change%':>8}")
        lines.append("-" * 55)
        for tick in ticks[:30]:
            side = "BUY" if tick.get("side") == "bu" else "SELL"
            lines.append(
                f"{tick.get('time', ''):>10}  "
                f"{tick.get('price', 0):>10,}  "
                f"{tick.get('vol', 0):>10,}  "
                f"{side:>4}  "
                f"{_pct(tick.get('priceChangePercent', 0)):>8}"
            )

    lines.append(
        "\n# Note: SSI iBoard provides realtime intraday data. "
        "For multi-day historical OHLCV, use yfinance with ticker suffix .VN (e.g. ACB.VN)"
    )
    return "\n".join(lines)


def get_indicators(
    symbol: Annotated[str, "Vietnam stock ticker"],
    indicator: Annotated[str, "Technical indicator name"],
    curr_date: Annotated[str, "Current trading date YYYY-MM-DD"],
    look_back_days: Annotated[int, "Number of days to look back"] = 30,
) -> str:
    """Return indicator note — SSI iBoard provides intraday data only."""
    symbol_upper = symbol.upper()
    try:
        quote = _fetch_quote(symbol_upper)
        ticks = _fetch_ticks(symbol_upper, page_size=100)
    except Exception as exc:
        return f"Error fetching SSI iBoard data for indicators: {exc}"

    prices = [t["price"] for t in reversed(ticks) if t.get("price")]
    if not prices:
        return f"No price data available for '{symbol}' to compute {indicator}."

    # Compute basic indicators from intraday prices
    avg = sum(prices) / len(prices)
    close = prices[-1]
    high = max(prices)
    low = min(prices)
    ref = quote.get("refPrice", 0)

    lines = [
        f"# {indicator} for {symbol_upper} (SSI iBoard – intraday session)",
        f"# Note: Multi-day technical indicators require historical data.",
        f"# Using today's {len(prices)} intraday price points as proxy.",
        "",
        f"Session Close/Last: {close:,} VND",
        f"Session Open: {quote.get('openPrice', 'N/A'):,} VND" if quote.get('openPrice') else "",
        f"Session High: {high:,} VND",
        f"Session Low: {low:,} VND",
        f"Session Average Price: {avg:,.0f} VND",
        f"Reference (Prev Close): {ref:,} VND",
        f"Intraday Range: {high - low:,} VND ({((high - low) / ref * 100) if ref else 0:.2f}%)",
        f"Price vs Ref: {_pct(quote.get('priceChangePercent', 0))}",
        "",
        f"Indicator Requested: {indicator}",
        f"Available: Session data only (SSI iBoard intraday). "
        f"For full {look_back_days}-day {indicator}, use yfinance with ticker ACB.VN",
    ]
    return "\n".join(l for l in lines if l is not None)


def get_fundamentals(
    ticker: Annotated[str, "Vietnam stock ticker"],
    curr_date: Annotated[str, "Current date (unused for SSI)"] = None,
) -> str:
    """Fetch company overview and market data from SSI iBoard."""
    symbol_upper = ticker.upper()
    try:
        quote = _fetch_quote(symbol_upper)
    except Exception as exc:
        return f"Error fetching SSI iBoard fundamentals for '{ticker}': {exc}"

    trading_date = quote.get("tradingDate", "")
    if len(trading_date) == 8:
        trading_date = f"{trading_date[:4]}-{trading_date[4:6]}-{trading_date[6:]}"

    lines = [
        f"# Fundamentals: {symbol_upper} (SSI iBoard)",
        f"## Company Info",
        f"Name (EN): {quote.get('companyNameEn', 'N/A')}",
        f"Name (VI): {quote.get('companyNameVi', 'N/A')}",
        f"ISIN: {quote.get('isin', 'N/A')}",
        f"Exchange: {quote.get('exchange', 'N/A').upper()}",
        f"Market: {quote.get('market', 'N/A')}",
        f"Stock Type: {quote.get('stockType', 'N/A')}",
        f"Par Value: {_vnd(quote.get('parValue', 0))}",
        f"Listed Shares: {int(quote.get('listedShare', 0)):,}" if quote.get('listedShare') else "",
        f"Trading Unit: {quote.get('tradingUnit', 100):,} shares",
        "",
        f"## Current Market Data (as of {trading_date})",
        f"Reference Price: {_vnd(quote.get('refPrice', 0))}",
        f"Ceiling: {_vnd(quote.get('ceiling', 0))}",
        f"Floor: {_vnd(quote.get('floor', 0))}",
        f"Last Price: {_vnd(quote.get('matchedPrice', 0))}",
        f"Open: {_vnd(quote.get('openPrice', 0))}",
        f"High: {_vnd(quote.get('highest', 0))}",
        f"Low: {_vnd(quote.get('lowest', 0))}",
        f"Change: {_vnd(quote.get('priceChange', 0))} ({_pct(quote.get('priceChangePercent', 0))})",
        f"Volume: {int(quote.get('nmTotalTradedQty', 0)):,} shares",
        f"Average Price: {_vnd(quote.get('avgPrice', 0))}",
        "",
        f"## Foreign Investment",
        f"Buy Volume: {int(quote.get('buyForeignQtty', 0)):,} shares",
        f"Sell Volume: {int(quote.get('sellForeignQtty', 0)):,} shares",
        f"Remaining Foreign Room: {int(quote.get('remainForeignQtty', 0)):,} shares",
        "",
        f"## Order Book",
        f"Best Bid: {_vnd(quote.get('best1Bid'))} x {int(quote.get('best1BidVol', 0)):,}",
        f"Best Ask: {_vnd(quote.get('best1Offer'))} x {int(quote.get('best1OfferVol', 0)):,}",
        f"Expected Matched Price: {_vnd(quote.get('expectedMatchedPrice', 0))}",
        f"Expected Matched Volume: {int(quote.get('expectedMatchedVolume', 0)):,}",
    ]
    return "\n".join(l for l in lines if l is not None)


def get_balance_sheet(
    ticker: Annotated[str, "Vietnam stock ticker"],
    freq: Annotated[str, "Reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "Current date"] = None,
) -> str:
    return (
        f"Balance sheet data for Vietnam stocks is not available via SSI iBoard realtime API. "
        f"For financial statements of {ticker.upper()}, refer to:\n"
        f"  - https://iboard.ssi.com.vn/dchart/chart/{ticker.upper()}\n"
        f"  - https://cafef.vn/thi-truong-chung-khoan/{ticker.lower()}.chn\n"
        f"  - https://vietstock.vn/{ticker.upper()}"
    )


def get_cashflow(
    ticker: Annotated[str, "Vietnam stock ticker"],
    freq: Annotated[str, "Reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "Current date"] = None,
) -> str:
    return (
        f"Cash flow data for Vietnam stocks is not available via SSI iBoard realtime API. "
        f"For financial statements of {ticker.upper()}, refer to cafef.vn or vietstock.vn."
    )


def get_income_statement(
    ticker: Annotated[str, "Vietnam stock ticker"],
    freq: Annotated[str, "Reporting frequency: annual/quarterly"] = "quarterly",
    curr_date: Annotated[str, "Current date"] = None,
) -> str:
    return (
        f"Income statement data for Vietnam stocks is not available via SSI iBoard realtime API. "
        f"For financial statements of {ticker.upper()}, refer to cafef.vn or vietstock.vn."
    )


def get_insider_transactions(
    ticker: Annotated[str, "Vietnam stock ticker"],
    curr_date: Annotated[str, "Current date"] = None,
) -> str:
    return (
        f"Insider transaction data is not available via SSI iBoard. "
        f"Check HOSE/HNX disclosures at https://cafef.vn or https://vietstock.vn/{ticker.upper()}"
    )


def get_news(
    ticker: Annotated[str, "Vietnam stock ticker"],
    start_date: Annotated[str, "Start date YYYY-MM-DD"],
    end_date: Annotated[str, "End date YYYY-MM-DD"],
) -> str:
    """Fetch recent news for a Vietnam stock with optional X social fallback."""
    symbol_upper = ticker.upper()
    x_block = build_x_tweet_news_block(symbol_upper, start_date, end_date)

    try:
        data = ssi_get("/news", params={"symbol": symbol_upper, "size": 20})
        if data.get("code") != "SUCCESS" or not data.get("data"):
            raise ValueError("empty")
        items = data["data"]
        lines = [f"# Recent News: {symbol_upper} (SSI iBoard)\n"]
        for item in items[:15]:
            title = item.get("title") or item.get("name", "")
            pub_date = item.get("publishDate") or item.get("date", "")
            source = item.get("source", "SSI")
            summary = (item.get("summary") or item.get("content", ""))[:200]
            if title:
                lines.append(f"**{pub_date}** [{source}] {title}")
                if summary:
                    lines.append(f"  {summary}")
                lines.append("")
        if x_block:
            lines.extend(["", x_block])
        return "\n".join(lines)
    except Exception:
        fallback = (
            f"News data for {symbol_upper} is not directly available via SSI iBoard API. "
            f"For Vietnam stock news, refer to:\n"
            f"  - https://cafef.vn/co-phieu-{symbol_upper.lower()}.chn\n"
            f"  - https://vietstock.vn/{symbol_upper}\n"
            f"  - https://tinnhanhchungkhoan.vn (general Vietnam market news)"
        )
        if x_block:
            return f"{fallback}\n\n{x_block}"
        return fallback


def get_global_news(
    curr_date: Annotated[str, "Current date YYYY-MM-DD"],
    look_back_days: Annotated[int, "Days to look back"] = 7,
    limit: Annotated[int, "Maximum number of items to return"] = 10,
) -> str:
    """Fetch Vietnam market overview from SSI iBoard group data.

    The `limit` parameter is accepted for tool-signature compatibility and is
    currently unused by the SSI iBoard source.
    """
    try:
        vn30 = ssi_get("/stock/group/VN30")
        hnx30 = ssi_get("/stock/group/HNX30")

        lines = [
            "# Vietnam Stock Market Overview (SSI iBoard)",
            f"# Date: {curr_date}",
            "",
        ]

        def _board_table(group_name: str, data: dict) -> list[str]:
            if data.get("code") != "SUCCESS" or not data.get("data"):
                return [f"No data available for {group_name}"]
            stocks = data["data"]
            rows = [f"\n## {group_name}", f"{'Symbol':>8}  {'Company':30}  {'Price':>10}  {'Change':>8}  {'Volume':>12}"]
            rows.append("-" * 76)
            for s in stocks[:15]:
                code = s.get("stockSymbol") or s.get("symbol", "")
                name = (s.get("companyNameEn") or "")[:28]
                price = s.get("matchedPrice") or s.get("lastPrice") or 0
                chg = s.get("priceChangePercent") or 0
                vol = s.get("nmTotalTradedQty") or s.get("stockVol") or 0
                rows.append(f"{code:>8}  {name:30}  {price:>10,}  {chg:>+7.2f}%  {int(vol):>12,}")
            return rows

        lines.extend(_board_table("VN30 (HOSE)", vn30))
        lines.extend(_board_table("HNX30 (HNX)", hnx30))
        lines.append(
            "\n## Market Context\n"
            "Vietnam stock market trades Monday–Friday, 09:00–14:30 ICT (GMT+7).\n"
            "For broader market news: cafef.vn, vietstock.vn, ndh.vn, tinnhanhchungkhoan.vn"
        )
        return "\n".join(lines)
    except Exception as exc:
        return f"Error fetching Vietnam market overview from SSI iBoard: {exc}"
