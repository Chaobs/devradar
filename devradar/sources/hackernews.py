"""Hacker News data source."""

from __future__ import annotations

import json
import urllib.request
from typing import Optional

from devradar.models import RadarItem, SourceType


HN_API = "https://hacker-news.firebaseio.com/v0"


def _hn_request(path: str) -> dict | list:
    url = f"{HN_API}/{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "DevRadar/0.1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_top_stories(min_points: int = 50, limit: int = 30) -> list[RadarItem]:
    """Fetch top HN stories, filtered by minimum points."""
    story_ids = _hn_request("topstories.json")[:100]  # fetch top 100 IDs, filter later

    items = []
    for sid in story_ids:
        if len(items) >= limit:
            break
        try:
            story = _hn_request(f"item/{sid}.json")
            if story.get("type") != "story" or story.get("deleted"):
                continue
            score = story.get("score", 0)
            if score < min_points:
                continue

            items.append(
                RadarItem(
                    title=story.get("title", "Untitled"),
                    url=story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    source=SourceType.HACKERNEWS,
                    description=f"HN discussion: {story.get('descendants', 0)} comments",
                    score=score,
                    author=story.get("by"),
                    created_at=_parse_hn_time(story.get("time")),
                )
            )
        except Exception:
            continue

    return items


def fetch_new_stories(min_points: int = 10, limit: int = 20) -> list[RadarItem]:
    """Fetch newest HN stories (good for early trend detection)."""
    story_ids = _hn_request("newstories.json")[:200]

    items = []
    for sid in story_ids:
        if len(items) >= limit:
            break
        try:
            story = _hn_request(f"item/{sid}.json")
            if story.get("type") != "story" or story.get("deleted"):
                continue
            score = story.get("score", 0)
            if score < min_points:
                continue

            items.append(
                RadarItem(
                    title=story.get("title", "Untitled"),
                    url=story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                    source=SourceType.HACKERNEWS,
                    description=f"New | {story.get('descendants', 0)} comments",
                    score=score,
                    author=story.get("by"),
                    created_at=_parse_hn_time(story.get("time")),
                )
            )
        except Exception:
            continue

    return items


def _parse_hn_time(timestamp: Optional[int]) -> Optional[object]:
    if not timestamp:
        return None
    from datetime import datetime, timezone

    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
