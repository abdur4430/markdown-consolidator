# Markdown Consolidator

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Intelligent consolidation and synthesis of multiple markdown files with overlapping content and different update dates.**

Designed for AI-assisted workflows where documentation becomes fragmented across multiple sessions—each AI interaction creates task-specific files that reference but don't update supporting documents, leading to scattered, overlapping knowledge.

## The Problem

```
Session 1: AI creates task-1.md, references config.md
Session 2: AI creates task-2.md, references config.md + task-1.md  
Session 3: AI creates task-3.md, references all above
...
Result: Overlapping content scattered across files, no re-synthesis
```

## The Solution

```bash
# One command to consolidate
mdconsolidate ./docs ./consolidated --strategy authority
```

**Before:** 47 fragmented markdown files with overlapping content  
**After:** 8 consolidated documents with full attribution and conflict resolution

## Features

- **Semantic Similarity Detection** - TF-IDF vectorization identifies content overlap
- **Section-Level Deduplication** - Fingerprinting catches exact duplicate sections
- **Multiple Clustering Methods** - Topic, temporal, hierarchical, or link-based grouping
- **Three Merge Strategies** - Authority (newest wins), Comprehensive (keep all), Canonical (single source)
- **Full Attribution** - Consolidated files track all sources and conflict resolutions
- **Validation Reports** - Coverage analysis and broken link detection

## Installation

### From PyPI (coming soon)

```bash
pip install markdown-consolidator
```

### From Source

```bash
git clone https://github.com/YOUR_USERNAME/markdown-consolidator.git
cd markdown-consolidator
pip install -e .
```

### As Claude Code Skill

Copy the `skill/` directory to your `.claude/skills/` folder:

```bash
cp -r skill/ ~/.claude/skills/markdown-consolidator/
```

## Quick Start

### Full Pipeline

```bash
# Consolidate a directory of markdown files
mdconsolidate ./docs ./consolidated

# With options
mdconsolidate ./docs ./consolidated \
    --strategy authority \
    --threshold 0.5 \
    --method topic
```

### Step by Step

```bash
# 1. Inventory files
mdconsolidate-inventory ./docs -o inventory.json

# 2. Analyze relationships
mdconsolidate-analyze inventory.json -o relationships.json

# 3. Cluster related files
mdconsolidate-cluster relationships.json -o clusters.json

# 4. Review clusters, then synthesize
mdconsolidate-synthesize clusters.json -o ./consolidated
```

### Python API

```python
from markdown_consolidator import consolidate

# Full pipeline
result = consolidate(
    source_dir="./docs",
    output_dir="./consolidated",
    strategy="authority",
    threshold=0.5
)

print(f"Created {result['files_created']} consolidated files")
print(f"Coverage: {result['coverage']}%")
```

## Merge Strategies

### Authority (default)

Most recently modified file is authoritative for conflicts. Best for evolving documentation.

```bash
mdconsolidate ./docs ./out --strategy authority
```

### Comprehensive

Preserves all unique information, flags conflicts for manual review. Best for knowledge bases.

```bash
mdconsolidate ./docs ./out --strategy comprehensive
```

### Canonical

Designates one file as the single source of truth. Best for specifications.

```bash
mdconsolidate ./docs ./out --strategy canonical
```

## Clustering Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| `topic` | Groups by content similarity | Default, general purpose |
| `temporal` | Groups by modification time | Sprint/session consolidation |
| `hierarchical` | Directory structure + similarity | Organized codebases |
| `links` | Internal reference patterns | Wikis, interconnected docs |
| `all` | Combines all methods | Maximum coverage |

```bash
mdconsolidate ./docs ./out --method temporal --window 7d
```

## Output Format

Consolidated files include full provenance:

```markdown
---
title: Authentication System
consolidated_from:
  - file: auth-design.md
    modified: 2024-12-01T10:30:00
  - file: oauth-notes.md
    modified: 2024-11-28T15:45:00
consolidated_at: 2024-12-03T14:00:00
strategy: authority
---

# Authentication System

<!-- SOURCE: auth-design.md:1-25 -->
## Overview
...

<!-- CONFLICT RESOLVED: Used auth-design.md (most recent) -->
Token expiry is set to 24 hours...
```

## Configuration

Create `.consolidator.yaml` in your project root:

```yaml
# Files to exclude
exclude:
  - "**/archive/**"
  - "**/.obsidian/**"
  - "**/templates/**"

# Similarity threshold (0-1)
similarity_threshold: 0.6

# Default strategy
default_strategy: authority

# Preserve originals
keep_originals: true
archive_path: .consolidated-archive/

# Frontmatter fields to preserve
preserve_frontmatter:
  - tags
  - aliases
  - created
```

## Integration

### Claude Code

Add to your `CLAUDE.md`:

```markdown
## Post-Task Consolidation

After completing tasks that modify documentation:
1. Run `mdconsolidate ./docs ./docs-consolidated`
2. Review validation report
3. Archive originals if successful
```

### GitHub Actions

```yaml
name: Consolidate Docs
on:
  push:
    paths: ['docs/**/*.md']
jobs:
  consolidate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install markdown-consolidator
      - run: mdconsolidate ./docs ./docs-consolidated
      - uses: peter-evans/create-pull-request@v6
        with:
          title: 'docs: Consolidate documentation'
```

### Obsidian

See [INTEGRATION.md](docs/INTEGRATION.md) for Obsidian vault setup and Dataview queries.

## Development

```bash
# Clone repo
git clone https://github.com/YOUR_USERNAME/markdown-consolidator.git
cd markdown-consolidator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check src/
```

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built to address the AI knowledge fragmentation problem in modern development workflows.

---

**Related Projects:**
- [Basic Memory](https://github.com/basicmachines-co/basic-memory) - Persistent LLM knowledge in markdown
- [Simone](https://github.com/Helmi/claude-simone) - Project management for Claude Code
