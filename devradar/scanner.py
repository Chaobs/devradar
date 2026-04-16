"""Core scanner — aggregate from all sources."""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from devradar.models import RadarItem, ScanResult, SourceType
from devradar.sources import fetch_trending, fetch_top_stories, fetch_new_stories, fetch_rss
from devradar.analyzers import score_items, classify_items


def scan_all(
    interests: list[str],
    github_languages: list[str] | None = None,
    hn_min_points: int = 50,
    rss_feeds: list[dict] | None = None,
    github_token: str | None = None,
    max_workers: int = 4,
) -> ScanResult:
    """Scan all configured sources concurrently."""

    github_languages = github_languages or ["python", "typescript"]
    rss_feeds = rss_feeds or []
    all_items: list[RadarItem] = []
    source_counts: dict[str, int] = {}

    def _fetch_github():
        items = []
        for lang in github_languages[:3]:  # limit to 3 langs
            items.extend(fetch_trending(language=lang, since="weekly", token=github_token))
        return items, "github"

    def _fetch_hn():
        return fetch_top_stories(min_points=hn_min_points), "hackernews"

    def _fetch_rss(feed: dict):
        return fetch_rss(feed["url"], feed.get("name")), f"rss:{feed.get('name', 'feed')}"

    # Run in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_fetch_github),
            executor.submit(_fetch_hn),
        ]
        for feed in rss_feeds:
            futures.append(executor.submit(_fetch_rss, feed))

        for future in as_completed(futures):
            try:
                items, source = future.result()
                all_items.extend(items)
                source_counts[source] = len(items)
            except Exception as e:
                # Log but continue
                print(f"Warning: Source fetch failed: {e}")

    # Dedupe by URL
    seen = set()
    unique_items = []
    for item in all_items:
        if item.url not in seen:
            seen.add(item.url)
            unique_items.append(item)

    # Score and classify
    scored = score_items(unique_items, interests)
    classified = classify_items(scored)

    return ScanResult(
        items=classified,
        scanned_at=datetime.now(),
        source_counts=source_counts,
    )


def quick_scan(interests: list[str], github_token: str | None = None) -> ScanResult:
    """Fast scan — GitHub trending only."""
    all_items = fetch_trending(language=None, since="weekly", token=github_token)
    scored = score_items(all_items, interests)
    classified = classify_items(scored)

    return ScanResult(
        items=classified,
        scanned_at=datetime.now(),
        source_counts={"github": len(all_items)},
    )
