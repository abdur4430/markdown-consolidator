# Integration Patterns

## Claude Code Integration

### CLAUDE.md Configuration

Add to your project's CLAUDE.md:

```markdown
## Knowledge Base Management

### Post-Task Consolidation

After completing tasks that create or modify markdown documentation:

1. Check if new files were created in `/docs`, `/notes`, or `/knowledge`
2. Run consolidation if fragmentation detected:
   ```bash
   python /path/to/consolidator/scripts/consolidate.py ./docs ./docs-consolidated
   ```
3. Review validation report for conflicts
4. Archive original files if consolidation successful

### Consolidation Triggers

Run consolidation when:
- More than 5 related markdown files exist in a directory
- A major feature is completed
- Before documentation review
- Weekly maintenance

### Slash Command

Use `/project:consolidate` to run the full pipeline:
```markdown
# .claude/commands/consolidate.md
Run markdown consolidation:
1. Inventory all markdown files in project
2. Analyze for overlapping content
3. Create consolidated versions
4. Generate validation report
```
```

### Hook Integration

Create a post-task hook:

```python
# .claude/hooks/post_task.py
import subprocess
from pathlib import Path

def should_consolidate(changed_files):
    """Check if consolidation is needed."""
    md_files = [f for f in changed_files if f.endswith('.md')]
    return len(md_files) >= 3

def run_consolidation():
    """Run the consolidation pipeline."""
    subprocess.run([
        'python', 'scripts/consolidate.py',
        './docs', './docs-consolidated',
        '--strategy', 'authority'
    ])

def on_task_complete(task_result):
    if should_consolidate(task_result.get('files_modified', [])):
        print("📚 Running knowledge base consolidation...")
        run_consolidation()
```

## Basic Memory Integration

### Output Format Compatibility

Generate Basic Memory compatible output:

```bash
python scripts/synthesize.py clusters.json --format basic-memory
```

Produces files with observation/relation syntax:

```markdown
---
title: Authentication System
type: note
permalink: authentication-system
tags:
  - security
  - api
---

## Key Concepts

- [definition] JWT (JSON Web Token) is the authentication mechanism
- [implementation] Token validation uses RS256 algorithm #security
- [decision] Token expiry set to 24 hours (balance security/UX)

## Relations

- implements [[API Security]]
- relates_to [[User Sessions]]
- depends_on [[Key Management]]
```

### Bidirectional Sync

Keep consolidated files in sync with Basic Memory:

```python
# sync_with_basic_memory.py
from basic_memory import MemoryClient

def sync_consolidated(consolidated_dir, memory_project):
    client = MemoryClient(project=memory_project)
    
    for md_file in consolidated_dir.glob('*.md'):
        # Parse consolidated file
        content = md_file.read_text()
        
        # Extract observations
        observations = extract_observations(content)
        
        # Extract relations  
        relations = extract_relations(content)
        
        # Sync to Basic Memory
        client.write_note(
            title=md_file.stem,
            observations=observations,
            relations=relations
        )
```

## Obsidian Integration

### Folder Structure

Recommended Obsidian vault structure:

```
vault/
├── 00-inbox/           # Raw AI-generated notes
├── 10-active/          # Current working documents
├── 20-consolidated/    # Output from consolidator
├── 30-archive/         # Original files post-consolidation
└── _consolidator/      # Working files (add to .gitignore)
```

### Automated Workflow

Create Templater script for consolidation:

```javascript
// .obsidian/scripts/consolidate.js
const { exec } = require('child_process');

async function runConsolidation() {
    const vaultPath = app.vault.adapter.basePath;
    const source = `${vaultPath}/00-inbox`;
    const output = `${vaultPath}/20-consolidated`;
    
    return new Promise((resolve, reject) => {
        exec(
            `python consolidator/scripts/consolidate.py "${source}" "${output}"`,
            (error, stdout, stderr) => {
                if (error) reject(error);
                else resolve(stdout);
            }
        );
    });
}

module.exports = runConsolidation;
```

### Dataview Integration

Query consolidated files:

```dataview
TABLE 
    consolidated_at as "Consolidated",
    length(consolidated_from) as "Sources"
FROM "20-consolidated"
WHERE consolidated_from
SORT consolidated_at DESC
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/consolidate.yml
name: Documentation Consolidation

on:
  push:
    paths:
      - 'docs/**/*.md'
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  consolidate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install pyyaml
      
      - name: Run consolidation
        run: |
          python scripts/consolidate.py \
            ./docs \
            ./docs-consolidated \
            --strategy authority \
            --threshold 0.5
      
      - name: Check for changes
        id: changes
        run: |
          if [[ -n $(git status --porcelain docs-consolidated/) ]]; then
            echo "changed=true" >> $GITHUB_OUTPUT
          fi
      
      - name: Create PR
        if: steps.changes.outputs.changed == 'true'
        uses: peter-evans/create-pull-request@v6
        with:
          title: 'docs: Consolidate documentation'
          body: |
            Automated documentation consolidation.
            
            Please review the validation report and resolve any flagged conflicts.
          branch: docs/consolidation
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: check-consolidation
        name: Check for documentation fragmentation
        entry: python scripts/check_fragmentation.py
        language: python
        files: \.md$
        pass_filenames: false
```

```python
# scripts/check_fragmentation.py
import sys
from pathlib import Path
from inventory import inventory_directory

def check_fragmentation(threshold=10):
    """Warn if too many small related markdown files."""
    docs = Path('docs')
    if not docs.exists():
        return 0
    
    inventory = inventory_directory(docs)
    
    # Check for many small files
    small_files = [f for f in inventory if f.get('word_count', 0) < 200]
    
    if len(small_files) > threshold:
        print(f"⚠️  Found {len(small_files)} small markdown files")
        print("Consider running consolidation: python scripts/consolidate.py docs docs-out")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(check_fragmentation())
```

## API Integration

### REST Wrapper

```python
# api/consolidator_api.py
from fastapi import FastAPI, BackgroundTasks
from pathlib import Path
import uuid

app = FastAPI()
jobs = {}

@app.post("/consolidate")
async def start_consolidation(
    source_path: str,
    output_path: str,
    strategy: str = "authority",
    background_tasks: BackgroundTasks
):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending"}
    
    background_tasks.add_task(
        run_consolidation_job,
        job_id,
        source_path,
        output_path,
        strategy
    )
    
    return {"job_id": job_id}

@app.get("/consolidate/{job_id}")
async def get_job_status(job_id: str):
    return jobs.get(job_id, {"error": "Job not found"})
```

### MCP Server

```python
# mcp_server.py
"""
MCP server for markdown consolidation.
Exposes consolidation tools to Claude.
"""

from mcp import Server, Tool

server = Server("markdown-consolidator")

@server.tool()
async def consolidate_directory(
    source: str,
    output: str,
    strategy: str = "authority"
) -> dict:
    """Consolidate markdown files in a directory."""
    # Run consolidation pipeline
    result = run_pipeline(source, output, strategy)
    return result

@server.tool()
async def analyze_fragmentation(directory: str) -> dict:
    """Analyze a directory for documentation fragmentation."""
    inventory = inventory_directory(Path(directory))
    # Return analysis
    return {
        "file_count": len(inventory),
        "avg_word_count": sum(f['word_count'] for f in inventory) / len(inventory),
        "recommendation": "consolidate" if needs_consolidation(inventory) else "ok"
    }
```
