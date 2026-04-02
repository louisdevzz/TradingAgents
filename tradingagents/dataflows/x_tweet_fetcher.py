"""Bridge for optional X/Twitter social signal fallback via x-tweet-fetcher.

This module is intentionally defensive:
- It does not hard-fail if the helper script is missing.
- It returns empty output on runtime or parsing errors.
- It only uses stdlib so no extra dependencies are required.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _resolve_fetcher_script() -> Path | None:
    """Resolve fetch_tweet.py location from env override or default repo path."""
    env_path = os.getenv("X_TWEET_FETCHER_SCRIPT", "").strip()
    if env_path:
        script_path = Path(env_path).expanduser().resolve()
        return script_path if script_path.is_file() else None

    repo_root = Path(__file__).resolve().parents[2]
    default_path = repo_root / ".temp" / "x-tweet-fetcher" / "scripts" / "fetch_tweet.py"
    return default_path if default_path.is_file() else None


def _clean_text(value: str, max_len: int = 240) -> str:
    compact = " ".join((value or "").split())
    if len(compact) <= max_len:
        return compact
    return f"{compact[: max_len - 3]}..."


def build_x_tweet_news_block(
    ticker: str,
    start_date: str,
    end_date: str,
    limit: int = 10,
) -> str:
    """Fetch and format social signals for ticker from x-tweet-fetcher.

    Returns a markdown block or an empty string when unavailable.
    """
    script_path = _resolve_fetcher_script()
    if script_path is None:
        return ""

    query = f"{ticker} stock OR {ticker} chứng khoán"
    cmd = [
        sys.executable,
        str(script_path),
        "--search",
        query,
        "--limit",
        str(limit),
        "--lang",
        "en",
    ]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except Exception:
        return ""

    if not proc.stdout.strip():
        return ""

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return ""

    tweets = payload.get("tweets")
    if not isinstance(tweets, list) or not tweets:
        return ""

    lines = [
        f"## Social Signals from X (x-tweet-fetcher), from {start_date} to {end_date}",
        f"Query: {query}",
        "",
    ]

    for item in tweets[:limit]:
        text = _clean_text(str(item.get("text", "")))
        if not text:
            continue
        author = item.get("author") or item.get("author_name") or "unknown"
        time_ago = item.get("time_ago", "")
        likes = int(item.get("likes", 0) or 0)
        replies = int(item.get("replies", 0) or 0)
        views = int(item.get("views", 0) or 0)
        lines.append(f"- [{author}] {text}")
        lines.append(f"  Engagement: likes={likes}, replies={replies}, views={views}; time={time_ago}")

    if len(lines) <= 3:
        return ""

    return "\n".join(lines)
