"""RSS/Atom feed data source."""

from __future__ import annotations

from typing import Optional

from devradar.models import RadarItem, SourceType


def fetch_rss(url: str, name: Optional[str] = None, limit: int = 20) -> list[RadarItem]:
    """Fetch items from an RSS or Atom feed."""
    try:
        import feedparser
    except ImportError:
        # Fallback: basic XML parsing without feedparser
        return _fetch_rss_fallback(url, name, limit)

    feed = feedparser.parse(url)
    items = []

    for entry in feed.entries[:limit]:
        title = entry.get("title", "Untitled")
        link = entry.get("link", "")
        summary = entry.get("summary", entry.get("description", ""))[:200]

        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            from datetime import datetime

            try:
                published = datetime(*entry.published_parsed[:6])
            except Exception:
                pass

        items.append(
            RadarItem(
                title=title,
                url=link,
                source=SourceType.RSS,
                description=summary,
                score=0,  # RSS doesn't have native scoring
                author=entry.get("author"),
                created_at=published,
                topics=[name] if name else [],
            )
        )

    return items


def _fetch_rss_fallback(
    url: str, name: Optional[str] = None, limit: int = 20
) -> list[RadarItem]:
    """Fallback RSS fetcher without feedparser dependency."""
    import json
    import urllib.request
    import xml.etree.ElementTree as ET

    req = urllib.request.Request(url, headers={"User-Agent": "DevRadar/0.1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode("utf-8", errors="replace")

    root = ET.fromstring(content)
    items = []

    # Handle both RSS and Atom feeds
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    # Try RSS format first
    for item in root.iter("item")[:limit]:
        title = _get_text(item, "title") or "Untitled"
        link = _get_text(item, "link") or ""
        desc = _get_text(item, "description") or ""
        items.append(
            RadarItem(
                title=title,
                url=link,
                source=SourceType.RSS,
                description=desc[:200],
                topics=[name] if name else [],
            )
        )

    # Try Atom format
    if not items:
        for entry in root.findall("atom:entry", ns)[:limit]:
            title_el = entry.find("atom:title", ns)
            link_el = entry.find("atom:link", ns)
            summary_el = entry.find("atom:summary", ns) or entry.find("atom:content", ns)

            title = title_el.text if title_el is not None else "Untitled"
            link = link_el.get("href", "") if link_el is not None else ""
            desc = summary_el.text[:200] if summary_el is not None and summary_el.text else ""

            items.append(
                RadarItem(
                    title=title,
                    url=link,
                    source=SourceType.RSS,
                    description=desc,
                    topics=[name] if name else [],
                )
            )

    return items


def _get_text(element, tag: str) -> Optional[str]:
    child = element.find(tag)
    return child.text if child is not None and child.text else None
