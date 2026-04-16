"""Tests for DevRadar."""

import pytest
from devradar.models import RadarItem, SourceType, ScanResult
from devradar.analyzers.scorer import score_item, classify_item


def test_radar_item():
    item = RadarItem(
        title="test/repo",
        url="https://github.com/test/repo",
        source=SourceType.GITHUB,
        description="A test repository",
        score=1000,
        language="Python",
        topics=["ai", "testing"],
    )
    assert item.title == "test/repo"
    assert item.source == SourceType.GITHUB
    assert "ai" in item.topics


def test_score_item():
    item = RadarItem(
        title="awesome-ai-project",
        url="https://github.com/test/awesome-ai-project",
        source=SourceType.GITHUB,
        description="An AI-powered tool for Python developers",
        score=500,
        language="Python",
        topics=["ai", "python"],
    )

    interests = ["ai", "python", "developer-tools"]
    score = score_item(item, interests)

    # Should have high score due to multiple matches
    assert score > 0.5
    assert score <= 1.0


def test_classify_item():
    item = RadarItem(
        title="llm-code-assistant",
        url="https://github.com/test/llm-code-assistant",
        source=SourceType.GITHUB,
        description="AI agent for code generation",
        score=1000,
        language="Python",
        topics=["ai", "llm", "agent"],
    )

    category = classify_item(item)
    assert category == "AI / ML"


def test_scan_result_top():
    items = [
        RadarItem(title="a", url="http://a", source=SourceType.GITHUB, score=100, relevance_score=0.9),
        RadarItem(title="b", url="http://b", source=SourceType.GITHUB, score=200, relevance_score=0.5),
        RadarItem(title="c", url="http://c", source=SourceType.GITHUB, score=50, relevance_score=0.95),
    ]

    result = ScanResult(items=items)
    top = result.top(2)

    # Should be sorted by combined score
    assert len(top) == 2
    assert top[0].title == "c"  # highest relevance
    assert top[1].title == "a"
