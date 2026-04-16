"""AI-powered summarizer — optional, requires OpenAI-compatible API."""

from __future__ import annotations

from typing import Optional, Sequence

from devradar.models import RadarItem, Briefing


def _get_client(api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini"):
    """Get an OpenAI-compatible client. Lazy import to avoid hard dependency."""
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key, base_url=base_url), model
    except ImportError:
        raise RuntimeError(
            "AI features require the 'openai' package. Install with: pip install devradar[ai]"
        )


def summarize_items(items: list[RadarItem], interests: Sequence[str], api_key: str,
                    base_url: str = "https://api.openai.com/v1",
                    model: str = "gpt-4o-mini") -> str:
    """Generate an AI summary of trending items."""
    client, model = _get_client(api_key, base_url, model)

    # Build context from items
    items_text = "\n".join(
        f"- [{item.title}]({item.url}) ({item.source.value}, score:{item.score}) "
        f"{item.description[:100]}"
        for item in items[:20]
    )

    prompt = f"""You are a tech analyst. Based on these trending developer items, write a concise briefing.

My interests: {', '.join(interests)}

Trending items:
{items_text}

Provide:
1. A 2-3 sentence overall summary of what's trending
2. Top 3 highlights with brief explanation of why each matters
3. Any emerging trends or patterns you notice
4. 1-2 recommendations for projects/tools to check out

Keep it concise and actionable. No filler."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def analyze_repo(item: RadarItem, api_key: str,
                 base_url: str = "https://api.openai.com/v1",
                 model: str = "gpt-4o-mini") -> str:
    """Generate an AI analysis of a specific repo."""
    client, model = _get_client(api_key, base_url, model)

    prompt = f"""Analyze this GitHub project briefly:

Name: {item.title}
Description: {item.description}
Stars: {item.score}
Language: {item.language}
Topics: {', '.join(item.topics)}

Provide:
1. What problem does it solve? (1 sentence)
2. Why is it popular? (1 sentence)
3. Who should use it? (1 sentence)
4. Potential concerns or limitations (1 sentence)"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def generate_briefing(items: list[RadarItem], interests: Sequence[str],
                      api_key: str, base_url: str = "https://api.openai.com/v1",
                      model: str = "gpt-4o-mini") -> Briefing:
    """Generate a full AI-powered daily briefing."""
    client, model = _get_client(api_key, base_url, model)

    items_text = "\n".join(
        f"- {item.title} | {item.source.value} | score:{item.score} | {item.description[:80]}"
        for item in items[:25]
    )

    prompt = f"""Generate a developer intelligence briefing.

User interests: {', '.join(interests)}

Today's items:
{items_text}

Return a JSON object with:
- "summary": 2-3 sentence overall summary
- "trends": list of 3-5 trending topic strings
- "recommendations": list of 2-3 actionable recommendations

JSON only, no markdown."""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.3,
    )

    import json
    try:
        data = json.loads(response.choices[0].message.content or "{}")
    except json.JSONDecodeError:
        data = {
            "summary": response.choices[0].message.content or "No summary available.",
            "trends": [],
            "recommendations": [],
        }

    return Briefing(
        summary=data.get("summary", ""),
        highlights=items[:5],
        trends=data.get("trends", []),
        recommendations=data.get("recommendations", []),
    )
