# Contributing to Markdown Consolidator

Thank you for your interest in contributing! This document provides guidelines for contributions.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/markdown-consolidator.git
   cd markdown-consolidator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Run tests:
   ```bash
   pytest
   ```

## Code Style

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting:

```bash
# Check code
ruff check src/

# Format code
ruff format src/
```

## Type Hints

All functions should have type hints. Use mypy for checking:

```bash
mypy src/
```

## Testing

- Write tests for new features
- Maintain test coverage above 80%
- Run the full test suite before submitting PRs:

```bash
pytest --cov=markdown_consolidator
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests and linting
6. Commit with descriptive messages
7. Push and create a Pull Request

## Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(clustering): add hierarchical clustering method`
- `fix(inventory): handle files with invalid UTF-8`
- `docs: update installation instructions`

## Reporting Issues

When reporting bugs, please include:

1. Python version
2. Operating system
3. Steps to reproduce
4. Expected vs actual behavior
5. Sample files (if applicable)

## Feature Requests

Feature requests are welcome! Please:

1. Check existing issues first
2. Describe the use case
3. Explain expected behavior
4. Consider implementation complexity

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
