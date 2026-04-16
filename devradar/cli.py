"""DevRadar CLI — AI-powered developer intelligence radar."""

from __future__ import annotations

import json
import os
import sys
from typing import Optional

import click
from rich.console import Console

from devradar import __version__
from devradar.config import load_config, save_config, init_config, DEFAULT_CONFIG_PATH
from devradar.models import DevRadarConfig
from devradar.scanner import scan_all, quick_scan
from devradar.output import (
    render_items, render_briefing, render_repo_detail, render_scan_summary,
    render_items_markdown, render_briefing_markdown,
)
from devradar.analyzers import analyze_repo, generate_briefing
from devradar.sources import fetch_repo_info

console = Console()


def _get_github_token() -> Optional[str]:
    return os.environ.get("GITHUB_TOKEN")


def _get_ai_config(config: DevRadarConfig) -> tuple[bool, str, str, str]:
    ai = config.ai
    enabled = ai.get("enabled", False)
    api_key = ai.get("api_key") or os.environ.get("OPENAI_API_KEY", "")
    model = ai.get("model", "gpt-4o-mini")
    base_url = ai.get("base_url", "https://api.openai.com/v1")
    return enabled, api_key, model, base_url


@click.group()
@click.version_option(version=__version__, prog_name="devradar")
def cli():
    """DevRadar - AI-powered developer intelligence radar.

    Aggregate, analyze, and track tech trends from GitHub, Hacker News, and more.
    """
    pass


@cli.command()
def init():
    """Interactive setup — choose interests & configure sources."""
    init_config()


@cli.command()
@click.option("--language", "-l", help="Filter by programming language")
@click.option("--since", type=click.Choice(["daily", "weekly", "monthly"]), default="weekly")
@click.option("--limit", "-n", default=20, help="Number of items to show")
def trending(language: Optional[str], since: str, limit: int):
    """GitHub trending repos."""
    from devradar.sources import fetch_trending

    with console.status("[cyan]Fetching GitHub trending...[/cyan]"):
        items = fetch_trending(language=language, since=since, token=_get_github_token())

    config = load_config()
    from devradar.analyzers import score_items, classify_items
    items = score_items(items, config.interests)
    items = classify_items(items)

    render_items(items[:limit], title=f"GitHub Trending ({since})")


@cli.command()
@click.option("--min-points", default=50, help="Minimum HN points")
@click.option("--limit", "-n", default=20, help="Number of stories")
def hn(min_points: int, limit: int):
    """Top Hacker News stories."""
    from devradar.sources import fetch_top_stories

    with console.status("[cyan]Fetching Hacker News...[/cyan]"):
        items = fetch_top_stories(min_points=min_points, limit=limit)

    config = load_config()
    from devradar.analyzers import score_items, classify_items
    items = score_items(items, config.interests)
    items = classify_items(items)

    render_items(items[:limit], title="Hacker News Top Stories")


@cli.command()
@click.option("--quick", "-q", is_flag=True, help="Quick scan (GitHub only)")
@click.option("--limit", "-n", default=30, help="Max items to show")
@click.option("--output", "-o", type=click.Choice(["terminal", "markdown", "json"]), default="terminal")
def scan(quick: bool, limit: int, output: str):
    """Scan all configured sources."""
    config = load_config()

    with console.status("[cyan]Scanning sources...[/cyan]"):
        if quick:
            result = quick_scan(config.interests, _get_github_token())
        else:
            gh_config = config.sources.get("github")
            hn_config = config.sources.get("hackernews")

            result = scan_all(
                interests=config.interests,
                github_languages=gh_config.languages if gh_config else ["python"],
                hn_min_points=hn_config.min_points if hn_config else 50,
                github_token=_get_github_token(),
            )

    top_items = result.top(limit)

    if output == "terminal":
        render_scan_summary(result)
        render_items(top_items)
    elif output == "markdown":
        print(render_items_markdown(top_items))
    elif output == "json":
        data = {
            "scanned_at": result.scanned_at.isoformat(),
            "total": result.total,
            "source_counts": result.source_counts,
            "items": [i.model_dump() for i in top_items],
        }
        print(json.dumps(data, indent=2, default=str))


@cli.command()
@click.option("--ai", is_flag=True, help="Enable AI-powered briefing")
@click.option("--output", "-o", type=click.Choice(["terminal", "markdown"]), default="terminal")
def briefing(ai: bool, output: str):
    """Generate daily briefing."""
    config = load_config()
    ai_enabled, api_key, model, base_url = _get_ai_config(config)

    with console.status("[cyan]Scanning sources...[/cyan]"):
        result = scan_all(
            interests=config.interests,
            github_token=_get_github_token(),
        )

    top_items = result.top(20)

    if ai and ai_enabled and api_key:
        with console.status("[cyan]Generating AI briefing...[/cyan]"):
            from devradar.analyzers import generate_briefing
            brief = generate_briefing(top_items, config.interests, api_key, base_url, model)

        if output == "terminal":
            render_briefing(brief)
        else:
            print(render_briefing_markdown(brief))
    else:
        # Non-AI briefing
        if output == "terminal":
            render_items(top_items, title="DevRadar Briefing")
        else:
            print(render_items_markdown(top_items, title="DevRadar Briefing"))


@cli.command()
@click.argument("repo")
@click.option("--ai", is_flag=True, help="AI analysis of the repo")
def analyze(repo: str, ai: bool):
    """Analyze a specific GitHub repo (owner/repo format)."""
    config = load_config()
    ai_enabled, api_key, model, base_url = _get_ai_config(config)

    with console.status(f"[cyan]Fetching {repo}...[/cyan]"):
        item = fetch_repo_info(repo, token=_get_github_token())

    if not item:
        console.print(f"[red]Error: Could not fetch repo '{repo}'[/red]")
        sys.exit(1)

    from devradar.analyzers import score_item, classify_item
    item.relevance_score = score_item(item, config.interests)
    item.category = classify_item(item)

    if ai and ai_enabled and api_key:
        with console.status("[cyan]Analyzing with AI...[/cyan]"):
            item.ai_summary = analyze_repo(item, api_key, base_url, model)

    render_repo_detail(item)


@cli.command()
def config():
    """Show current configuration."""
    cfg = load_config()
    console.print(f"\n[bold]Config file:[/bold] {DEFAULT_CONFIG_PATH}")
    console.print(f"[bold]Interests:[/bold] {', '.join(cfg.interests)}")
    console.print(f"[bold]Sources:[/bold]")
    for name, src in cfg.sources.items():
        console.print(f"  - {name}: {'enabled' if src.enabled else 'disabled'}")
    console.print(f"[bold]AI:[/bold] {'enabled' if cfg.ai.get('enabled') else 'disabled'}")
    console.print()


def main():
    cli()


if __name__ == "__main__":
    main()
