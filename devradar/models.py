"""Data models for DevRadar."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    GITHUB = "github"
    HACKERNEWS = "hackernews"
    PRODUCTHUNT = "producthunt"
    RSS = "rss"
    REDDIT = "reddit"


class RadarItem(BaseModel):
    """A single item from any data source."""

    title: str
    url: str
    source: SourceType
    description: str = ""
    score: int = 0  # stars / points / upvotes
    language: Optional[str] = None
    topics: list[str] = Field(default_factory=list)
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    # AI-enriched fields
    relevance_score: float = 0.0  # 0-1, how relevant to user's interests
    ai_summary: Optional[str] = None
    category: Optional[str] = None


class ScanResult(BaseModel):
    """Result of a full scan across all sources."""

    items: list[RadarItem]
    scanned_at: datetime = Field(default_factory=datetime.now)
    source_counts: dict[str, int] = Field(default_factory=dict)

    @property
    def total(self) -> int:
        return len(self.items)

    def top(self, n: int = 10) -> list[RadarItem]:
        """Get top N items by relevance + score."""
        scored = sorted(
            self.items,
            key=lambda x: (x.relevance_score * 50 + min(x.score / 100, 50)),
            reverse=True,
        )
        return scored[:n]

    def by_source(self, source: SourceType) -> list[RadarItem]:
        return [i for i in self.items if i.source == source]

    def by_category(self, category: str) -> list[RadarItem]:
        return [i for i in self.items if i.category == category]


class Briefing(BaseModel):
    """AI-generated daily briefing."""

    date: datetime = Field(default_factory=datetime.now)
    summary: str = ""
    highlights: list[RadarItem] = Field(default_factory=list)
    trends: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class SourceConfig(BaseModel):
    """Configuration for a data source."""

    enabled: bool = True
    # GitHub-specific
    languages: list[str] = Field(default_factory=lambda: ["python", "typescript"])
    since: str = "weekly"  # daily, weekly, monthly
    # HackerNews-specific
    min_points: int = 50
    # ProductHunt-specific
    topics: list[str] = Field(default_factory=lambda: ["developer-tools", "ai"])
    # RSS-specific
    url: Optional[str] = None
    name: Optional[str] = None


class DevRadarConfig(BaseModel):
    """Full DevRadar configuration."""

    interests: list[str] = Field(
        default_factory=lambda: ["ai", "python", "developer-tools", "open-source"]
    )
    sources: dict[str, SourceConfig] = Field(default_factory=dict)
    ai: dict = Field(
        default_factory=lambda: {
            "enabled": False,
            "model": "gpt-4o-mini",
            "base_url": "https://api.openai.com/v1",
        }
    )
    output: dict = Field(
        default_factory=lambda: {
            "format": "terminal",
            "max_items": 20,
        }
    )
