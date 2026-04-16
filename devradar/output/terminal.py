"""Rich terminal output renderer."""

from __future__ import annotations

from typing import Sequence

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.columns import Columns
from rich.text import Text

from devradar.models import RadarItem, ScanResult, Briefing

console = Console()


def render_items(items: list[RadarItem], title: str = "DevRadar Scan Results") -> None:
    """Render items as a rich table."""
    table = Table(
        title=title,
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
        title_style="bold white",
    )

    table.add_column("#", style="dim", width=3)
    table.add_column("Project", style="bold", min_width=25)
    table.add_column("Score", justify="right", width=8)
    table.add_column("Lang", style="cyan", width=10)
    table.add_column("Relevance", width=10)
    table.add_column("Category", style="magenta", width=12)
    table.add_column("Source", style="green", width=10)

    for i, item in enumerate(items, 1):
        relevance_bar = _relevance_bar(item.relevance_score)
        table.add_row(
            str(i),
            item.title[:35],
            f"{item.score:,}",
            item.language or "-",
            relevance_bar,
            item.category or "-",
            item.source.value,
        )

    console.print()
    console.print(table)


def render_briefing(briefing: Briefing) -> None:
    """Render an AI-generated briefing."""
    console.print()
    console.print(Panel(
        f"[bold]{briefing.summary}[/bold]",
        title="📡 DevRadar Daily Briefing",
        border_style="cyan",
        padding=(1, 2),
    ))

    if briefing.trends:
        console.print("\n[bold yellow]🔥 Emerging Trends[/bold yellow]")
        for trend in briefing.trends:
            console.print(f"  • {trend}")

    if briefing.highlights:
        console.print("\n[bold green]⭐ Top Highlights[/bold green]")
        for item in briefing.highlights[:5]:
            console.print(f"  [bold]{item.title}[/bold] ({item.source.value})")
            if item.description:
                console.print(f"    {item.description[:80]}")

    if briefing.recommendations:
        console.print("\n[bold blue]💡 Recommendations[/bold blue]")
        for rec in briefing.recommendations:
            console.print(f"  → {rec}")

    console.print()


def render_repo_detail(item: RadarItem) -> None:
    """Render detailed view of a single repo."""
    info = Text()
    info.append(f"{item.title}\n", style="bold cyan")
    info.append(f"URL: {item.url}\n", style="blue")
    info.append(f"Stars: {item.score:,}\n")
    info.append(f"Language: {item.language or 'N/A'}\n", style="cyan")
    info.append(f"Topics: {', '.join(item.topics) or 'None'}\n", style="green")
    info.append(f"Relevance: {_relevance_bar(item.relevance_score)}\n")
    info.append(f"\n{item.description}\n")

    if item.ai_summary:
        info.append(f"\n🧠 AI Analysis:\n{item.ai_summary}\n", style="yellow")

    console.print(Panel(info, border_style="cyan", padding=(1, 2)))


def render_scan_summary(result: ScanResult) -> None:
    """Render scan summary statistics."""
    console.print()
    console.print(Panel(
        f"[bold]Scanned {result.total} items[/bold]\n"
        + "\n".join(f"  {src}: {cnt}" for src, cnt in result.source_counts.items()),
        title="DevRadar Scan",
        border_style="blue",
    ))


def _relevance_bar(score: float) -> str:
    """Create a visual relevance bar."""
    filled = int(score * 10)
    bar = "#" * filled + "-" * (10 - filled)
    if score >= 0.7:
        return f"[green]{bar}[/green] {score:.1f}"
    elif score >= 0.3:
        return f"[yellow]{bar}[/yellow] {score:.1f}"
    else:
        return f"[dim]{bar}[/dim] {score:.1f}"
