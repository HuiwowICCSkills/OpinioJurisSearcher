"""Offline tests for OpinioJurisSearcher."""
from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import opiniojuris_adapter as adapter  # noqa: E402


class FakeHttp:
    def __init__(self):
        self.evidence = []

    def json(self, url, params=None, headers=None):
        return [{"id": 1, "link": "https://opiniojuris.org/post", "date_gmt": "2026-01-01T00:00:00",
                 "title": {"rendered": "State Immunity"}, "content": {"rendered": "<p>Body text</p>"}}], {
            "source_url": url, "http_status": 200, "content_type": "application/json",
            "bytes": 100, "retrieved_at": "2026-11-09T00:00:00Z", "sha256": "0" * 64,
            "total": "1", "total_pages": "1"}


def args(**kwargs):
    base = dict(limit=1, offset=0, cache=".cache", offline=False, cache_ttl=0, timeout=30)
    base.update(kwargs)
    return argparse.Namespace(**base)


class OpinioTests(unittest.TestCase):
    def test_search_returns_rendered_body(self):
        out = adapter.search("state immunity", args(), FakeHttp())
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["total"], 1)
        self.assertIn("Body text", out["results"][0]["text"])


if __name__ == "__main__":
    unittest.main()
