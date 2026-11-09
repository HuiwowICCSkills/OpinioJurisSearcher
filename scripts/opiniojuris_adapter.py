#!/usr/bin/env python3
"""Opinio Juris WordPress adapter for OpinioJurisSearcher."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from skillkit import HTTP, RetrievalError, clean, result

PROG = "opiniojuris_search.py"
DESCRIPTION = "Search the public Opinio Juris WordPress site."
CACHE_DEFAULT = ".opiniojuris-cache"
FETCH_TIMEOUT_DEFAULT = 300

API = "https://opiniojuris.org/wp-json/wp/v2/posts"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/155.0.0.0 Safari/537.36"
)


def _headers() -> dict[str, str]:
    return {"User-Agent": UA, "Accept": "application/json, text/html;q=0.9, */*;q=0.8"}


def make_http(args: argparse.Namespace) -> HTTP:
    return HTTP(
        args.cache,
        offline=args.offline,
        ttl=args.cache_ttl,
        timeout=args.timeout,
        user_agent=UA,
    )


def add_search_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=10, help="1..50 (default 10)")
    parser.add_argument("--offset", type=int, default=0, help=">= 0 (default 0)")


def add_fetch_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text-out", help="Write article text here")


def search(query: str, args: argparse.Namespace, http: HTTP) -> dict[str, Any]:
    if not query.strip():
        raise ValueError("A non-empty query is required")
    if not 1 <= args.limit <= 50:
        raise ValueError("limit must be 1..50")
    if args.offset < 0:
        raise ValueError("offset must be >= 0")
    data, meta = http.json(
        API,
        {"search": query, "per_page": args.limit, "offset": args.offset},
        headers=_headers(),
    )
    if not isinstance(data, list):
        raise RetrievalError("Opinio Juris WordPress schema changed: expected a post array")
    rows: list[dict[str, Any]] = []
    for post in data:
        body = post.get("content", {}).get("rendered", "")
        text = clean(body)
        rows.append(
            result(
                post.get("title", {}).get("rendered", ""),
                post.get("link", ""),
                "wordpress-api",
                text,
                kind="retrieved_text" if text else "retrieved_metadata",
                id=post.get("id"),
                published=post.get("date_gmt"),
                modified=post.get("modified_gmt"),
                author_id=post.get("author"),
                body_html=body,
                text=text,
                access="public rendered post body",
                content_scope="public WordPress post body; protected posts may omit content",
            )
        )
    total = meta.get("total")
    return {
        "status": "ok" if rows else "no-results-in-queried-index",
        "query": query,
        "total": int(total) if total not in (None, "") else None,
        "results": rows,
        "pagination": {
            "offset": args.offset,
            "limit": args.limit,
            "next_offset": args.offset + len(rows)
            if len(rows) == args.limit
            else None,
        },
        "scope": "Opinio Juris public WordPress search; rendered post bodies",
        "evidence": http.evidence,
    }


def fetch(locator: str, args: argparse.Namespace, http: HTTP) -> dict[str, Any]:
    parsed = urlparse(locator)
    if parsed.scheme != "https" or (parsed.hostname or "").lower() != "opiniojuris.org":
        raise ValueError("fetch expects an https://opiniojuris.org/ URL")
    soup, meta = http.soup(locator, headers=_headers())
    container = soup.select_one("article") or soup.select_one("main") or soup.body or soup
    for node in container.select("script, style, nav, header, footer, input, select, button, textarea, noscript"):
        node.decompose()
    text = container.get_text("\n", strip=True)
    if len(text) < 100:
        raise RetrievalError("Insufficient Opinio Juris article text")
    if args.text_out:
        Path(args.text_out).write_text(text, encoding="utf-8")
    return {
        "status": "ok",
        "url": meta["source_url"],
        "title": clean(soup.title.get_text(" ", strip=True)) if soup.title else "",
        "text": text,
        "text_characters": len(text),
        "content_scope": "Opinio Juris rendered article page text",
        "text_out": str(Path(args.text_out).resolve()) if args.text_out else None,
        "sha256": meta["sha256"],
        "retrieved_at": meta["retrieved_at"],
    }


def doctor(args: argparse.Namespace) -> dict[str, Any]:
    checks = [
        {"check": "python", "ok": True, "detail": "Python runtime available"},
        {"check": "requests", "ok": True, "detail": "requests importable"},
        {"check": "beautifulsoup4", "ok": True, "detail": "bs4 importable"},
    ]
    if args.no_probe:
        return {"ok": True, "status": "ok (probes skipped)", "checks": checks}
    http = make_http(args)
    try:
        data, meta = http.json(
            API,
            {"search": "state immunity", "per_page": 1, "offset": 0},
            headers=_headers(),
        )
        checks.append(
            {
                "check": "Opinio Juris WordPress API",
                "ok": isinstance(data, list),
                "posts": len(data) if isinstance(data, list) else None,
                "http_status": meta["http_status"],
                "bytes": meta["bytes"],
            }
        )
        ok = isinstance(data, list)
    except Exception as exc:
        checks.append({"check": "Opinio Juris WordPress API", "ok": False, "error": f"{type(exc).__name__}: {exc}"})
        ok = False
    return {"ok": ok, "status": "ok" if ok else "error", "checks": checks, "catalog": {"api": API}}
