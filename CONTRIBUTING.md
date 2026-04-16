# Contributing to DevRadar
# 为 DevRadar 做贡献

Thanks for your interest in contributing! We're glad you're here.
感谢你对贡献 DevRadar 感兴趣！我们很高兴你来了。

## Development Setup / 开发环境设置

```bash
# Clone the repo / 克隆仓库
git clone https://github.com/chaobs/devradar.git
cd devradar

# Install dev dependencies / 安装开发依赖
pip install -e ".[dev]"

# Run tests / 运行测试
pytest

# Lint / 代码检查
ruff check devradar/
```

## Project Structure / 项目结构

```
devradar/
├── sources/          # Data source connectors / 数据源连接器
│   ├── github.py     # GitHub Trending + API
│   ├── hackernews.py # HN API
│   └── rss.py        # Generic RSS/Atom
├── analyzers/        # Processing pipeline / 处理管道
│   ├── scorer.py     # Relevance scoring / 相关度评分
│   └── summarizer.py # AI summarization / AI 摘要
├── output/           # Rendering / 渲染
│   ├── terminal.py   # Rich terminal UI
│   └── markdown.py
├── scanner.py        # Core aggregation logic / 核心聚合逻辑
├── config.py         # Configuration management / 配置管理
├── models.py         # Pydantic data models / Pydantic 数据模型
└── cli.py            # Click CLI entry point / Click CLI 入口
```

## Adding a New Source / 添加新的数据源

1. Create `devradar/sources/yoursource.py` / 创建 `devradar/sources/yoursource.py`
2. Implement a `fetch_*` function returning `list[RadarItem]` / 实现返回 `list[RadarItem]` 的 `fetch_*` 函数
3. Add import to `devradar/sources/__init__.py` / 添加导入到 `devradar/sources/__init__.py`
4. Update `scanner.py` to call your source / 更新 `scanner.py` 调用你的数据源
5. Add tests in `tests/test_sources.py` / 在 `tests/test_sources.py` 添加测试

## Coding Style / 编码风格

- Use ruff for linting: `ruff check devradar/` / 使用 ruff 检查代码: `ruff check devradar/`
- Type hints on all public functions / 所有公共函数都要类型提示
- Docstrings for modules and major functions / 模块和主要函数要有文档字符串
- Keep functions focused and under 50 lines / 保持函数专注，不超过 50 行

## Testing / 测试

- Run tests: `pytest` / 运行测试: `pytest`
- Run with coverage: `pytest --cov=devradar` / 运行并查看覆盖率: `pytest --cov=devradar`
- Write tests for new sources and analyzers / 为新的数据源和分析器写测试

## Pull Requests / 提交 Pull Request

1. Fork the repo / Fork 仓库
2. Create a feature branch: `git checkout -b feature/my-feature` / 创建功能分支: `git checkout -b feature/my-feature`
3. Make your changes with tests / 带着测试做修改
4. Run lint and tests: `ruff check && pytest` / 运行检查和测试: `ruff check && pytest`
5. Submit a PR with a clear description / 提交带有清晰描述的 PR

## Ideas for Contributions / 贡献想法

- New data sources (Reddit/r/programming, DevTo, Lobsters, Product Hunt API)
- 新数据源（Reddit/r/programming、DevTo、Lobsters、Product Hunt API）
- Web dashboard mode / Web 仪表盘模式
- Historical trend tracking database / 历史趋势追踪数据库
- More output formats (HTML, PDF) / 更多输出格式（HTML、PDF）
- Plugin system for custom analyzers / 自定义分析器插件系统
- Better AI prompts and classification / 更好的 AI 提示词和分类

## Code of Conduct / 行为准则

- Be respectful and inclusive / 保持尊重和包容
- Follow the existing code style / 遵循现有代码风格
- Write tests for new features / 为新功能写测试
- Update documentation when needed / 需要时更新文档

## Questions? / 有问题？

- Open an issue for bugs or feature requests / 提交 issue 报告 bug 或功能请求
- Join the discussion in discussions / 在 discussions 中参与讨论
- Read existing issues before creating new ones / 创建新 issue 前先看看已有的

Thank you for making DevRadar better!
感谢你让 DevRadar 变得更好！
