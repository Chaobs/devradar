"""GitHub data source — trending repos + search API."""

from __future__ import annotations

import json
import re
import urllib.request
from typing import Optional

from devradar.models import RadarItem, SourceType


GITHUB_API = "https://api.github.com"


def _gh_request(url: str, token: Optional[str] = None) -> dict | list:
    """Make an authenticated GitHub API request."""
    headers = {
        "User-Agent": "DevRadar/0.1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_trending(
    language: Optional[str] = None,
    since: str = "weekly",
    token: Optional[str] = None,
) -> list[RadarItem]:
    """Fetch trending repositories from GitHub via search API.

    Uses the GitHub Search API to approximate trending behavior:
    - Sort by stars for repos created recently
    - Filter by language if specified
    - Filter by time range (daily/weekly/monthly)
    """
    # Map 'since' to date range
    from datetime import datetime, timedelta

    since_days = {"daily": 1, "weekly": 7, "monthly": 30}
    days = since_days.get(since, 7)
    since_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Build query
    query_parts = [f"created:>{since_date}"]
    if language:
        query_parts.append(f"language:{language}")

    query = "+".join(query_parts)
    url = f"{GITHUB_API}/search/repositories?q={query}&sort=stars&order=desc&per_page=30"

    data = _gh_request(url, token)
    items = []
    for repo in data.get("items", []):
        desc = repo.get("description") or ""
        items.append(
            RadarItem(
                title=repo["full_name"],
                url=repo["html_url"],
                source=SourceType.GITHUB,
                description=desc[:200],
                score=repo["stargazers_count"],
                language=repo.get("language"),
                topics=repo.get("topics", []),
                author=repo.get("owner", {}).get("login"),
                created_at=_parse_github_date(repo.get("created_at")),
            )
        )
    return items


def fetch_repo_info(full_name: str, token: Optional[str] = None) -> Optional[RadarItem]:
    """Fetch detailed info about a specific repo."""
    url = f"{GITHUB_API}/repos/{full_name}"
    try:
        repo = _gh_request(url, token)
        return RadarItem(
            title=repo["full_name"],
            url=repo["html_url"],
            source=SourceType.GITHUB,
            description=(repo.get("description") or "")[:200],
            score=repo["stargazers_count"],
            language=repo.get("language"),
            topics=repo.get("topics", []),
            author=repo.get("owner", {}).get("login"),
            created_at=_parse_github_date(repo.get("created_at")),
        )
    except Exception:
        return None


def fetch_user_starred(username: str, token: Optional[str] = None) -> list[RadarItem]:
    """Fetch repos starred by a user (inspiration feed)."""
    url = f"{GITHUB_API}/users/{username}/starred?per_page=30&sort=created&direction=desc"
    try:
        repos = _gh_request(url, token)
        items = []
        for repo in repos:
            items.append(
                RadarItem(
                    title=repo["full_name"],
                    url=repo["html_url"],
                    source=SourceType.GITHUB,
                    description=(repo.get("description") or "")[:200],
                    score=repo["stargazers_count"],
                    language=repo.get("language"),
                    topics=repo.get("topics", []),
                    created_at=_parse_github_date(repo.get("starred_at")),
                )
            )
        return items
    except Exception:
        return []


def _parse_github_date(date_str: Optional[str]) -> Optional[object]:
    """Parse ISO date string from GitHub API."""
    if not date_str:
        return None
    from datetime import datetime

    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
