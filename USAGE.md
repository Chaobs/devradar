# DevRadar User Guide / DevRadar 使用指南

> Complete guide to using DevRadar - from installation to advanced usage
> DevRadar 完整使用指南 - 从安装到高级使用

---

## Table of Contents / 目录

1. [Installation / 安装](#installation--安装)
2. [Quick Start / 快速开始](#quick-start--快速开始)
3. [Commands Reference / 命令参考](#commands-reference--命令参考)
4. [Configuration / 配置](#configuration--配置)
5. [Advanced Usage / 高级用法](#advanced-usage--高级用法)
6. [FAQ / 常见问题](#faq--常见问题)

---

## Installation / 安装

### Requirements / 要求

- Python 3.9 or higher / Python 3.9 或更高版本
- Windows, macOS, or Linux / Windows、macOS 或 Linux
- Internet connection / 网络连接

### Install from PyPI / 从 PyPI 安装

```bash
pip install devradar
```

### Install from Source / 从源码安装

```bash
git clone https://github.com/chaobs/devradar.git
cd devradar
pip install -e .
```

### Verify Installation / 验证安装

```bash
devradar --version
# Output: devradar, version 0.1.0
```

---

## Quick Start / 快速开始

### Step 1: Initial Setup / 步骤 1：初始设置

Run the interactive setup to configure your interests:
运行交互式设置来配置你的兴趣：

```bash
devradar init
```

This will create a config file at `~/.devradar/config.yaml` with default settings.
这将在 `~/.devradar/config.yaml` 创建配置文件，包含默认设置。

### Step 2: Scan Everything / 步骤 2：扫描全部

```bash
# Quick scan (GitHub only) / 快速扫描（仅 GitHub）
devradar scan --quick

# Full scan (GitHub + Hacker News) / 完整扫描（GitHub + Hacker News）
devradar scan
```

### Step 3: Get Your Briefing / 步骤 3：获取简报

```bash
devradar briefing
```

This generates a personalized report based on your configured interests.
这会根据你配置的兴产生个性化报告。

---

## Commands Reference / 命令参考

### devradar init

Interactive setup wizard.
交互式设置向导。

```bash
devradar init
```

You'll be prompted to:
系统会提示你：

- Select your interests / 选择你的兴趣
- Configure data sources / 配置数据源
- Enable/disable AI features / 启用/禁用 AI 功能

### devradar scan

Scan all configured sources and display results.
扫描所有已配置的数据源并显示结果。

```bash
# Default scan / 默认扫描
devradar scan

# Quick scan (faster) / 快速扫描（更快）
devradar scan --quick

# Limit results / 限制结果数量
devradar scan --limit 10

# Output formats / 输出格式
devradar scan --output terminal  # Default / 默认
devradar scan --output json       # JSON format / JSON 格式
devradar scan --output markdown  # Markdown format / Markdown 格式
```

### devradar trending

View GitHub trending repositories.
查看 GitHub 趋势仓库。

```bash
# All languages / 所有语言
devradar trending

# Specific language / 指定语言
devradar trending --language python
devradar trending --language typescript
devradar trending --language rust

# Time range / 时间范围
devradar trending --since daily    # Today / 今天
devradar trending --since weekly   # This week / 本周
devradar trending --since monthly  # This month / 本月

# Combine options / 组合选项
devradar trending --language python --since weekly --limit 10
```

### devradar hn

Get top Hacker News stories.
获取 Hacker News 热门故事。

```bash
# Default (top 10 stories) / 默认（10 条热门故事）
devradar hn

# Custom limit / 自定义数量
devradar hn --limit 20

# Minimum points filter / 最低分数筛选
devradar hn --min-points 100

# Combine options / 组合选项
devradar hn --limit 15 --min-points 50
```

### devradar briefing

Generate a daily briefing of important tech news.
生成每日技术新闻简报。

```bash
# Default briefing / 默认简报
devradar briefing

# With AI analysis / 带 AI 分析
devradar briefing --ai

# Output as Markdown / 输出为 Markdown
devradar briefing --output markdown

# Combine options / 组合选项
devradar briefing --ai --output markdown
```

### devradar analyze

Analyze a specific GitHub repository.
分析特定的 GitHub 仓库。

```bash
# Basic analysis / 基本分析
devradar analyze facebook/react

# With AI summary / 带 AI 摘要
devradar analyze facebook/react --ai

# Any public repository / 任何公开仓库
devradar analyze microsoft/vscode
devradar analyze tensorflow/tensorflow
```

### devradar config

View current configuration.
查看当前配置。

```bash
devradar config
```

Output example / 输出示例：
```
Config file: C:\Users\YourName\.devradar\config.yaml
Interests: ai, python, developer-tools, open-source
Sources:
  - github: enabled
  - hackernews: enabled
AI: disabled
```

---

## Configuration / 配置

### Config File Location / 配置文件位置

- Windows: `C:\Users\<YourName>\.devradar\config.yaml`
- macOS/Linux: `~/.devradar/config.yaml`

### Manual Configuration / 手动配置

Edit the config file directly:
直接编辑配置文件：

```yaml
# ~/.devradar/config.yaml

# Your interests (affects relevance scoring) / 你的兴趣（影响相关度评分）
interests:
  - ai
  - python
  - developer-tools
  - open-source
  - rust

# Data sources configuration / 数据源配置
sources:
  github:
    enabled: true
    languages: [python, typescript, rust]
    since: weekly
  hackernews:
    enabled: true
    min_points: 50

# AI configuration (optional) / AI 配置（可选）
ai:
  enabled: false
  model: gpt-4o-mini
  base_url: https://api.openai.com/v1

# Output configuration / 输出配置
output:
  max_items: 20
```

### Environment Variables / 环境变量

```bash
# GitHub API token (increases rate limit) / GitHub API token（提高 API 限制）
export GITHUB_TOKEN=your-github-token

# OpenAI API key / OpenAI API 密钥
export OPENAI_API_KEY=your-openai-key
```

On Windows:
在 Windows 上：

```powershell
$env:GITHUB_TOKEN = "your-github-token"
$env:OPENAI_API_KEY = "your-openai-key"
```

---

## Advanced Usage / 高级用法

### Piping Output / 管道输出

```bash
# Save as JSON / 保存为 JSON
devradar scan --output json > trends.json

# Save as Markdown / 保存为 Markdown
devradar briefing --output markdown > daily-report.md

# Process with jq / 用 jq 处理
devradar scan --output json | jq '.items[0].title'

# Search in results / 在结果中搜索
devradar scan --output json | Select-String "python"
```

### Cron Job Setup / 定时任务设置

Schedule DevRadar to run daily:
安排 DevRadar 每天运行：

```bash
# Linux/macOS (crontab) / Linux/macOS (crontab)
# Run at 8 AM every day / 每天早上 8 点运行
0 8 * * * devradar briefing --output markdown >> ~/devradar-reports/$(date +\%Y-\%m-\%d).md

# Windows Task Scheduler / Windows 任务计划程序
# Create a task to run: devradar briefing --output markdown
```

### Custom RSS Sources / 自定义 RSS 源

Add to config:
添加到配置：

```yaml
sources:
  rss:
    - name: "Hacker News"
      url: "https://hnrss.org/frontpage"
    - name: "TechCrunch AI"
      url: "https://techcrunch.com/category/artificial-intelligence/feed/"
    - name: "Reddit r/programming"
      url: "https://www.reddit.com/r/programming/.rss"
```

### GitHub Token Setup / GitHub Token 设置

1. Go to https://github.com/settings/tokens
2. Generate a new token (classic)
3. Select scopes: `public_repo`, `read:user`
4. Use the token in config or environment variable

See: https://github.com/settings/tokens

### API Rate Limits / API 速率限制

| Source | Without Token | With Token |
|--------|--------------|------------|
| GitHub | 60 requests/hour | 5,000 requests/hour |
| Hacker News | 10,000 requests/15min | N/A |

---

## FAQ / 常见问题

### Q: How does DevRadar score relevance? / DevRadar 如何计算相关度？

A: DevRadar uses keyword matching against your configured interests. It analyzes repository names, descriptions, topics, and programming languages to calculate a 0.0-1.0 relevance score.
DevRadar 使用关键词匹配你配置的兴来分析仓库名称、描述、主题和编程语言，计算 0.0-1.0 的相关度评分。

### Q: Why is Hacker News slow? / 为什么 Hacker News 很慢？

A: HN's official API doesn't exist. DevRadar uses web scraping which is slower than API-based sources. Use `--limit` to reduce the number of items fetched.
HN 没有官方 API。DevRadar 使用网页抓取，比基于 API 的数据源慢。使用 `--limit` 减少获取的项目数量。

### Q: Can I use DevRadar without AI? / 没有 AI 能用 DevRadar 吗？

A: Yes! All core features work without AI. AI features are opt-in and require an OpenAI-compatible API key.
可以！所有核心功能都无需 AI 即可工作。AI 功能是可选的，需要 OpenAI 兼容的 API 密钥。

### Q: How to update DevRadar? / 如何更新 DevRadar？

```bash
pip install --upgrade devradar
```

### Q: How to uninstall? / 如何卸载？

```bash
pip uninstall devradar
# Optionally remove config / 可选删除配置
rm -rf ~/.devradar
```

### Q: Why are some Chinese characters garbled? / 为什么有些中文字符是乱码？

A: This is a Windows console encoding issue. The underlying data is correct. Use `--output json` to get clean data without display issues.
这是 Windows 控制台编码问题。底层数据是正确的。使用 `--output json` 获取无显示问题的干净数据。

### Q: How to report bugs? / 如何报告 Bug？

1. Check existing issues / 检查已有的 issues
2. Create a new issue with: / 创建新 issue，包含：
   - DevRadar version / DevRadar 版本 (`devradar --version`)
   - Command that failed / 失败的命令
   - Full error message / 完整错误信息
   - Steps to reproduce / 复现步骤

### Q: Can I contribute? / 我可以贡献代码吗？

A: Absolutely! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
当然可以！查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解更多指南。

---

## Tips & Tricks / 技巧

1. **Use aliases** / 使用别名
   ```bash
   alias dr="devradar"
   dr scan --quick
   ```

2. **Combine with other tools** / 与其他工具结合
   ```bash
   devradar trending --language python --limit 5 | clip
   ```

3. **Daily workflow** / 日常工作流
   ```bash
   # Morning check / 早晨查看
   devradar briefing
   
   # When researching / 研究时
   devradar analyze owner/repo
   
   # Weekly trend check / 每周趋势检查
   devradar trending --since weekly --limit 10
   ```

4. **Custom scripts** / 自定义脚本
   ```bash
   # Create a script for daily reports
   # 创建每日报告脚本
   #!/bin/bash
   mkdir -p ~/devradar-reports
   devradar briefing --output markdown > ~/devradar-reports/$(date +%Y-%m-%d).md
   ```

---

## Support / 支持

- GitHub Issues: https://github.com/chaobs/devradar/issues
- Documentation: https://github.com/chaobs/devradar#readme

---

**Happy coding and happy scouting!**
**编程快乐，侦察愉快！**
