"""Markdown output renderer."""

from __future__ import annotations

from devradar.models import RadarItem, ScanResult, Briefing


def render_items_markdown(items: list[RadarItem], title: str = "DevRadar Report") -> str:
    """Render items as Markdown."""
    lines = [f"# {title}\n"]

    # Group by category
    categories: dict[str, list[RadarItem]] = {}
    for item in items:
        cat = item.category or "Other"
        categories.setdefault(cat, []).append(item)

    for cat, cat_items in sorted(categories.items()):
        lines.append(f"\n## {cat}\n")
        lines.append("| # | Project | Stars | Language | Relevance | Description |")
        lines.append("|---|---------|-------|----------|-----------|-------------|")
        for i, item in enumerate(cat_items, 1):
            lines.append(
                f"| {i} | [{item.title}]({item.url}) | {item.score:,} "
                f"| {item.language or '-'} | {item.relevance_score:.1f} "
                f"| {item.description[:60]} |"
            )

    return "\n".join(lines)


def render_briefing_markdown(briefing: Briefing) -> str:
    """Render briefing as Markdown."""
    lines = [f"# DevRadar Daily Briefing — {briefing.date.strftime('%Y-%m-%d')}\n"]

    lines.append(f"## Summary\n\n{briefing.summary}\n")

    if briefing.trends:
        lines.append("## Emerging Trends\n")
        for trend in briefing.trends:
            lines.append(f"- {trend}")
        lines.append("")

    if briefing.highlights:
        lines.append("## Top Highlights\n")
        for item in briefing.highlights:
            lines.append(f"- **[{item.title}]({item.url})** ({item.source.value}) — {item.description[:80]}")
        lines.append("")

    if briefing.recommendations:
        lines.append("## Recommendations\n")
        for rec in briefing.recommendations:
            lines.append(f"- {rec}")
        lines.append("")

    return "\n".join(lines)
