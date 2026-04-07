#!/usr/bin/env python3
"""Fetch recent papers from arXiv RSS feeds.

Usage:
    python scripts/fetch_arxiv.py              # output JSON to stdout
    python scripts/fetch_arxiv.py -o out.json  # output to file
    python scripts/fetch_arxiv.py --hours 48   # fetch last 48h (default: 24h)
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone

import feedparser

CATEGORIES = ["cs.LG", "cs.CV", "cs.CL", "cs.AI", "stat.ML"]


def fetch_recent(hours: int = 24) -> list[dict]:
    """Fetch papers from arXiv RSS feeds for the given categories."""
    papers = []
    for cat in CATEGORIES:
        feed = feedparser.parse(f"https://arxiv.org/rss/{cat}")
        for entry in feed.entries:
            papers.append({
                "title": entry.get("title", "").strip().replace("\n", " "),
                "abstract": entry.get("summary", "").strip(),
                "authors": [a.get("name", "") for a in entry.get("authors", [])],
                "arxiv_url": entry.get("link", ""),
                "arxiv_id": _extract_id(entry.get("link", "")),
                "category": cat,
                "published": entry.get("published", ""),
            })
    # Deduplicate by arxiv_url
    seen = set()
    unique = []
    for p in papers:
        if p["arxiv_url"] not in seen:
            seen.add(p["arxiv_url"])
            unique.append(p)
    return unique


def _extract_id(url: str) -> str:
    """Extract arXiv ID from URL like https://arxiv.org/abs/2106.09685v2."""
    parts = url.rstrip("/").split("/")
    raw = parts[-1] if parts else ""
    # Strip version suffix (e.g., v2)
    if "v" in raw:
        raw = raw[: raw.rfind("v")]
    return raw


def main():
    parser = argparse.ArgumentParser(description="Fetch recent arXiv papers via RSS")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    parser.add_argument("--hours", type=int, default=24, help="Fetch papers from last N hours")
    parser.add_argument("--categories", nargs="+", help="Override arXiv categories")
    args = parser.parse_args()

    if args.categories:
        global CATEGORIES
        CATEGORIES = args.categories

    papers = fetch_recent(hours=args.hours)
    output = json.dumps(papers, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Fetched {len(papers)} papers → {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
