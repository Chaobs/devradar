"""Configuration management for DevRadar."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import yaml

from devradar.models import DevRadarConfig, SourceConfig

DEFAULT_CONFIG_DIR = Path.home() / ".devradar"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / "config.yaml"


def load_config(path: Optional[Path] = None) -> DevRadarConfig:
    """Load configuration from YAML file."""
    config_path = path or DEFAULT_CONFIG_PATH

    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return DevRadarConfig(**data)

    # Return defaults
    config = DevRadarConfig()
    config.sources = {
        "github": SourceConfig(enabled=True),
        "hackernews": SourceConfig(enabled=True, min_points=50),
    }
    return config


def save_config(config: DevRadarConfig, path: Optional[Path] = None) -> Path:
    """Save configuration to YAML file."""
    config_path = path or DEFAULT_CONFIG_PATH
    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w", encoding="utf-8") as f:
        yaml.dump(config.model_dump(), f, default_flow_style=False, allow_unicode=True)

    return config_path


def init_config() -> DevRadarConfig:
    """Interactive configuration setup."""
    from rich.console import Console
    from rich.prompt import Prompt, Confirm

    console = Console()
    console.print("\n[bold cyan]DevRadar Setup[/bold cyan]\n")

    config = DevRadarConfig()

    # Interests
    interests_input = Prompt.ask(
        "[bold]Your interests[/bold] (comma-separated)",
        default="ai, python, developer-tools, open-source",
    )
    config.interests = [i.strip() for i in interests_input.split(",")]

    # GitHub
    if Confirm.ask("Enable GitHub Trending?", default=True):
        langs = Prompt.ask("Languages (comma-separated)", default="python, typescript")
        gh_config = SourceConfig(
            enabled=True,
            languages=[l.strip() for l in langs.split(",")],
            since="weekly",
        )
        config.sources["github"] = gh_config

    # Hacker News
    if Confirm.ask("Enable Hacker News?", default=True):
        min_pts = Prompt.ask("Minimum points", default="50")
        config.sources["hackernews"] = SourceConfig(
            enabled=True,
            min_points=int(min_pts),
        )

    # AI
    if Confirm.ask("Enable AI features? (requires OpenAI API key)", default=False):
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if not api_key:
            api_key = Prompt.ask("OpenAI API Key", password=True)
        config.ai = {
            "enabled": True,
            "model": Prompt.ask("Model", default="gpt-4o-mini"),
            "base_url": "https://api.openai.com/v1",
            "api_key": api_key,
        }

    # Save
    path = save_config(config)
    console.print(f"\n[green]✓ Configuration saved to {path}[/green]\n")

    return config
