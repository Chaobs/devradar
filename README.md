# DevRadar

> AI-powered developer intelligence radar - aggregate, analyze, and track tech trends from GitHub, Hacker News, Product Hunt, and more.
>
> AI 驱动的开发者情报雷达 - 聚合、分析和追踪来自 GitHub、Hacker News、Product Hunt 等平台的技术趋势。

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/chaobs/devradar.svg)](https://github.com/chaobs/devradar/stargazers)

**Stop doom-scrolling tech Twitter. Let DevRadar do the scouting.**
**告别刷推特焦虑，让 DevRadar 替你侦察。**

DevRadar is a CLI tool that aggregates developer intelligence from multiple sources, uses AI to analyze trends, and delivers a personalized tech briefing - right in your terminal.
DevRadar 是一个命令行工具，聚合多个来源的开发者情报，使用 AI 分析趋势，并在终端中为你提供个性化的技术简报。

## Why DevRadar? / 为什么选择 DevRadar?

- Multi-source aggregation - GitHub Trending, Hacker News, Product Hunt, Reddit, RSS feeds
- 多源聚合 - GitHub 趋势、Hacker News、Product Hunt、Reddit、RSS 订阅
- AI-powered analysis - Summarize, classify, and score projects by relevance to YOUR interests
- AI 驱动的分析 - 根据你的兴趣总结、分类和评分项目
- Personalized radar - Define your tech stack and interests, get only what matters
- 个性化雷达 - 定义你的技术栈和兴趣，只获取重要的内容
- Trend detection - Spot rising projects before they hit mainstream
- 趋势检测 - 在项目成为主流之前发现它们
- Daily briefing - Auto-generated morning report of what's new in your world
- 每日简报 - 自动生成的早间报告，告诉你世界里发生了什么
- Beautiful terminal UI - Rich-formatted output, no browser needed
- 美观的终端界面 - 富文本格式输出，无需浏览器

## Quick Start / 快速开始

```bash
# Install / 安装
pip install devradar

# First run - interactive setup / 首次运行 - 交互式设置
devradar init

# Scan all sources now / 立即扫描所有数据源
devradar scan

# Get today's briefing / 获取今日简报
devradar briefing

# Watch mode - live updates / 监视模式 - 实时更新
devradar watch

# Add a custom source / 添加自定义源
devradar source add https://example.com/rss
```

## Commands / 命令

| Command | Description | 描述 |
|---------|-------------|------|
| `devradar init` | Interactive setup - choose interests & configure sources | 交互式设置 - 选择兴趣并配置数据源 |
| `devradar scan` | Aggregate from all configured sources | 聚合所有已配置的数据源 |
| `devradar briefing` | Generate AI-powered daily briefing | 生成 AI 驱动的每日简报 |
| `devradar watch` | Live monitoring with auto-refresh | 实时监控，自动刷新 |
| `devradar trending` | GitHub trending repos (language/time filter) | GitHub 趋势仓库（语言/时间筛选） |
| `devradar hn` | Top Hacker News stories with AI summary | Hacker News 热门故事，AI 摘要 |
| `devradar source` | Manage information sources (add/remove/list) | 管理数据源（添加/删除/列表） |
| `devradar config` | View/edit configuration | 查看/编辑配置 |
| `devradar export` | Export report as Markdown/JSON/HTML | 导出报告为 Markdown/JSON/HTML |
| `devradar analyze <owner/repo>` | Analyze a specific GitHub repository | 分析特定的 GitHub 仓库 |

## AI Features (Optional) / AI 功能（可选）

DevRadar works great without AI. But with an OpenAI-compatible API key:
DevRadar 无需 AI 也能很好地工作。但如果配置 OpenAI 兼容的 API 密钥：

```bash
# Set your API key / 设置你的 API 密钥
export OPENAI_API_KEY=sk-...

# AI-powered briefing with personalized analysis / AI 驱动的个性化简报
devradar briefing --ai

# Get AI score for a specific project / 获取特定项目的 AI 评分
devradar analyze owner/repo
```

AI features / AI 功能:
- Smart summarization - Condense 50-item feeds into 5-sentence briefings
- 智能摘要 - 将 50 条内容压缩成 5 句话的简报
- Relevance scoring - Rate each item against your configured interests
- 相关度评分 - 根据你配置的兴趣对每条内容评分
- Trend prediction - Identify which new projects are likely to blow up
- 趋势预测 - 识别哪些新项目可能会爆发
- Cross-source analysis - "This HN topic matches a GitHub repo trending in Python"
- 跨源分析 - "这个 HN 话题与 Python 趋势中的一个 GitHub 仓库匹配"

## Configuration / 配置

Config file / 配置文件: `~/.devradar/config.yaml`

```yaml
interests:
  - ai-agents
  - python
  - developer-tools
  - open-source
  
sources:
  github:
    enabled: true
    languages: [python, typescript, rust]
    since: weekly
  hackernews:
    enabled: true
    min_points: 100
  producthunt:
    enabled: true
    topics: [developer-tools, ai]
  rss:
    - name: "TechCrunch AI"
      url: "https://techcrunch.com/category/artificial-intelligence/feed/"

ai:
  enabled: true
  model: gpt-4o-mini
  base_url: https://api.openai.com/v1

output:
  format: terminal  # terminal | markdown | json | html
  max_items: 20
```

## Architecture / 架构

```
DevRadar
├── sources/          # Data source connectors / 数据源连接器
│   ├── github.py     # GitHub Trending + API
│   ├── hackernews.py # HN API
│   ├── producthunt.py
│   └── rss.py        # Generic RSS/Atom
├── analyzers/        # Processing pipeline / 处理管道
│   ├── classifier.py # Tag & categorize items / 标签和分类
│   ├── scorer.py     # Relevance scoring / 相关度评分
│   ├── summarizer.py # AI summarization / AI 摘要
│   └── tracker.py    # Trend detection over time / 趋势追踪
├── output/           # Rendering / 渲染
│   ├── terminal.py   # Rich terminal UI
│   ├── markdown.py
│   └── html.py
└── cli.py            # Click-based CLI
```

## Development / 开发

```bash
# Clone / 克隆
git clone https://github.com/chaobs/devradar.git
cd devradar

# Setup / 设置
pip install -e ".[dev]"

# Run tests / 运行测试
pytest

# Lint / 代码检查
ruff check devradar/
```

## Contributing / 贡献

Contributions are welcome! Especially:
欢迎贡献！特别欢迎：

- New data source connectors (Reddit, DevTo, Lobsters, etc.)
- 新的数据源连接器（Reddit、DevTo、Lobsters 等）
- AI analysis plugins / AI 分析插件
- Output format templates / 输出格式模板
- Bug fixes & improvements / Bug 修复和改进

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多指南。

## License / 许可证

MIT License - see [LICENSE](LICENSE) for details.
MIT 许可证 - 查看 [LICENSE](LICENSE) 了解更多详情。

---

**Built with care for developers who'd rather code than scroll.**
**为那些宁愿写代码也不想刷推的开发者精心打造。**
