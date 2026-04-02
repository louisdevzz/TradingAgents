import json
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from tradingagents.dataflows.x_tweet_fetcher import build_x_tweet_news_block


class XTweetFallbackTests(unittest.TestCase):
    def test_returns_empty_when_script_unavailable(self):
        with patch("tradingagents.dataflows.x_tweet_fetcher._resolve_fetcher_script", return_value=None):
            block = build_x_tweet_news_block("DGC", "2026-03-27", "2026-04-02")
        self.assertEqual(block, "")

    def test_formats_tweets_when_cli_returns_json(self):
        payload = {
            "tweets": [
                {
                    "author": "@analyst_vn",
                    "text": "DGC breakout with strong foreign buying",
                    "likes": 12,
                    "replies": 3,
                    "views": 440,
                    "time_ago": "2h",
                }
            ]
        }
        proc = SimpleNamespace(stdout=json.dumps(payload))

        with patch("tradingagents.dataflows.x_tweet_fetcher._resolve_fetcher_script", return_value=__file__):
            with patch("tradingagents.dataflows.x_tweet_fetcher.subprocess.run", return_value=proc):
                block = build_x_tweet_news_block("DGC", "2026-03-27", "2026-04-02", limit=5)

        self.assertIn("Social Signals from X", block)
        self.assertIn("DGC stock OR DGC chứng khoán", block)
        self.assertIn("@analyst_vn", block)
        self.assertIn("likes=12, replies=3, views=440", block)


if __name__ == "__main__":
    unittest.main()
