"""Relevance scorer — rate items against user interests."""

from __future__ import annotations

import re
from typing import Sequence

from devradar.models import RadarItem


# Keyword mapping: interest -> related terms
INTEREST_KEYWORDS: dict[str, list[str]] = {
    "ai": ["artificial-intelligence", "machine-learning", "deep-learning", "llm", "gpt",
           "neural", "transformer", "ai-agent", "ai-tool", "claude", "gemini", "copilot"],
    "python": ["python", "django", "flask", "fastapi", "pytorch", "pandas", "numpy"],
    "developer-tools": ["cli", "terminal", "ide", "editor", "devtools", "debugger",
                        "linter", "formatter", "ci-cd", "developer-experience"],
    "open-source": ["open-source", "oss", "foss", "mit-license", "apache-license"],
    "rust": ["rust", "cargo", "wasm", "webassembly"],
    "typescript": ["typescript", "javascript", "nodejs", "deno", "bun", "react", "vue"],
    "devops": ["kubernetes", "docker", "terraform", "cloud", "aws", "gcp", "azure"],
    "security": ["security", "vulnerability", "cve", "encryption", "authentication"],
    "database": ["database", "sql", "nosql", "postgres", "redis", "mongodb"],
    "web": ["web", "frontend", "backend", "api", "rest", "graphql", "http"],
}


def score_item(item: RadarItem, interests: Sequence[str]) -> float:
    """Score an item's relevance to user interests. Returns 0.0-1.0.

    Scoring heuristic:
    - Exact interest keyword match in title: +0.3
    - Interest keyword match in description: +0.15
    - Topic tag match: +0.25
    - Language match: +0.15
    - Partial keyword match: +0.05 each
    """
    score = 0.0
    text = f"{item.title} {item.description}".lower()
    item_topics = [t.lower() for t in item.topics]
    item_lang = (item.language or "").lower()

    for interest in interests:
        interest_lower = interest.lower()
        keywords = INTEREST_KEYWORDS.get(interest_lower, [interest_lower])

        # Direct interest match in title
        if interest_lower in item.title.lower():
            score += 0.3

        # Direct interest match in description
        if interest_lower in item.description.lower():
            score += 0.15

        # Keyword matches
        for kw in keywords:
            if kw.lower() in text:
                score += 0.05

        # Topic match
        if interest_lower in item_topics:
            score += 0.25

        # Language match
        if interest_lower == item_lang:
            score += 0.15

    return min(score, 1.0)


def score_items(items: list[RadarItem], interests: Sequence[str]) -> list[RadarItem]:
    """Score all items and return sorted by relevance."""
    for item in items:
        item.relevance_score = score_item(item, interests)

    items.sort(
        key=lambda x: (x.relevance_score, x.score),
        reverse=True,
    )
    return items


def classify_item(item: RadarItem) -> str:
    """Classify an item into a broad category."""
    text = f"{item.title} {item.description} {' '.join(item.topics)}".lower()

    categories = {
        "AI / ML": ["ai", "machine-learning", "deep-learning", "llm", "gpt", "neural",
                     "agent", "nlp", "computer-vision"],
        "Dev Tools": ["cli", "terminal", "ide", "editor", "debugger", "linter", "formatter"],
        "Web / API": ["web", "frontend", "backend", "api", "http", "rest", "graphql"],
        "Infrastructure": ["kubernetes", "docker", "cloud", "devops", "terraform", "ci-cd"],
        "Data / DB": ["database", "sql", "data", "analytics", "etl", "pipeline"],
        "Security": ["security", "vulnerability", "encryption", "auth", "crypto"],
        "Mobile": ["mobile", "ios", "android", "react-native", "flutter", "swift"],
        "Education": ["tutorial", "course", "learn", "book", "guide", "curriculum"],
    }

    best_cat = "Other"
    best_score = 0

    for cat, keywords in categories.items():
        cat_score = sum(1 for kw in keywords if kw in text)
        if cat_score > best_score:
            best_score = cat_score
            best_cat = cat

    return best_cat


def classify_items(items: list[RadarItem]) -> list[RadarItem]:
    """Classify all items."""
    for item in items:
        item.category = classify_item(item)
    return items
