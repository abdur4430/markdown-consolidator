# CLAUDE.md - Advanced Context Engineering Configuration

This file configures Claude to use the advanced three-phase development workflow: Research → Plan → Implement.

## Repository Overview

This repository implements the advanced context engineering workflow for AI-driven development, based on the principles from the "Advanced Context Engineering for Coding Agents" methodology.

## Username Configuration

RPI commands automatically detect your username for file naming. Priority order:

1. **`.claude/config.yaml`** (recommended - per repository)
2. **`RPI_USERNAME`** environment variable (global default)
3. **`git config user.name`** (automatic fallback)
4. **"user"** (last resort default)

**Quick Setup:**
```bash
# Option 1: Create local config (recommended)
cat > .claude/config.yaml << EOF
username: benjamin
EOF

# Option 2: Set environment variable
export RPI_USERNAME="benjamin"

# Option 3: Use git username automatically (no setup needed)
git config user.name  # This will be auto-converted
```

Files will be named: `YYYY.MM.DD-{username}-description.md`

## Coding Standards Integration

The RPI workflow automatically loads coding standards from multiple sources:

### Priority Order:
1. **Environment**: `$MINTY_DOCS_PATH/cross-cutting/coding-standards/`
2. **Local**: `docs/coding-standards/` in the current repository

### Configuration:

**Option 1: Use external standards via environment variable**
```bash
# Set MINTY_DOCS_PATH to your external standards repository
export MINTY_DOCS_PATH="/path/to/your/standards-repo"
```

**Option 2: Use local standards (project-specific rules)**
```bash
mkdir -p docs/coding-standards
# Add your .md files with coding standards
```

**Option 3: No configuration needed**
- If no standards exist anywhere, commands continue gracefully
- No error messages or warnings

### Standards Format:
Standards should be markdown files containing:
- Code style guidelines
- Architectural patterns
- Anti-patterns to avoid
- Testing requirements

## Documentation Updates

The RPI workflow supports automatic documentation updates after implementation. Documentation can flow to two destinations:

### Destinations

| Type | Path | When to Use |
|------|------|-------------|
| Cross-cutting | `$MINTY_DOCS_PATH/cross-cutting/` | Patterns, standards, or behaviors affecting multiple repos |
| Repo-specific | `docs/` | Features, APIs, or behaviors specific to this repository |

### Workflow

After implementation completes, the `/implement` command will:

1. **Check** if documentation updates are warranted (new feature, changed behavior, new pattern)
2. **Determine** the appropriate destination based on scope:
   - Cross-cutting → `$MINTY_DOCS_PATH`
   - Repo-specific → `docs/`
3. **Prompt** for documentation if a destination exists
4. **Skip silently** if no documentation destination is configured

### Configuration

**For cross-cutting documentation:**
```bash
# Set in ~/.zshrc or ~/.bashrc
export MINTY_DOCS_PATH="/path/to/minty-docs"
```

**For repo-specific documentation:**
```bash
# Create docs directory in your repository
mkdir -p docs/
```

### Graceful Degradation

If neither `$MINTY_DOCS_PATH` is configured nor the `docs/` folder is populated:
- No errors or warnings are shown
- The workflow continues normally
- Users can add documentation manually later

This ensures the RPI workflow works for all users regardless of their documentation setup.

## Test-Driven Development (TDD)

The RPI workflow encourages TDD practices during implementation:

### Workflow:
1. **RED**: Write/update tests FIRST - tests must fail initially
2. **GREEN**: Write minimal code to make tests pass
3. **REFACTOR**: Clean up while keeping tests green

### Commit Strategy:
```
test: Phase N - add tests for [feature]     # RED
feat: Phase N - implement [feature]          # GREEN
refactor: Phase N - clean up [feature]       # REFACTOR
```

### Skill Integration:
The `/implement` command will invoke `superpowers:test-driven-development` skill (if available) to guide proper test-first development.

### Opting Out:
TDD is **strongly recommended** but can be bypassed if explicitly stated in the task. However, this should be rare and justified.

## Core Workflow

### The Three Phases

1. **Research Phase** (`/research`)
   - Understand how the existing system works
   - Identify relevant files and components
   - Pinpoint where changes are needed
   - Prevents misunderstanding that leads to bad code

2. **Planning Phase** (`/plan`)
   - Define every change to be made
   - Include affected files and code snippets
   - Specify verification steps
   - Much shorter than code changes but easier to review

3. **Implementation Phase** (`/implement`)
   - Execute based on the approved plan
   - Follow established patterns
   - Maintain context efficiency
   - Verify at each step

## Commands Available

### Primary Commands
- `/research [query]` - Conduct comprehensive codebase research
- `/plan [research-file or description]` - Create detailed implementation plan
- `/implement [plan-file]` - Execute the implementation plan

### Additional Commands
- `/epic-oneshot [task]` - Execute complete RPI workflow in one session
- `/standup` - Generate progress report from RPI artifacts
- `/blocked` - Identify and analyze implementation blockers
- `/create_handoff` - Create handoff documentation for session transfer
- `/resume_handoff [handoff-file]` - Resume work from handoff document

### Usage Examples
```bash
# Research how authentication works
/research How does the authentication system work?

# Create a plan based on research
/plan thoughts/research/2025.01.08-username-authentication-flow.md

# Implement the plan
/implement thoughts/plans/2025.01.08-username-add-oauth-support.md

# Create a handoff to transfer work to another session
/create_handoff

# Resume from a handoff
/resume_handoff thoughts/handoffs/2025.11.08-username-oauth-implementation.md
```

## Key Principles

### Context Management
- **Keep context under 40%** - Maintain efficiency by managing context carefully
- **Intentional compaction** - Actively shrink context to focus on what matters
- **Parallel sub-agents** - Use specialized agents for different research aspects
- **No shouting matches** - Good plans eliminate back-and-forth corrections

### Quality Standards
- **No slop** - Production-ready code only
- **Works in complex codebases** - Handles brownfield development
- **Mental alignment** - Plans are easier to review than PRs
- **Measurable success** - Clear verification criteria

## File Organization

```
project-root/
├── .claude/
│   ├── commands/       # Workflow commands
│   │   ├── research.md
│   │   ├── plan.md
│   │   ├── implement.md
│   │   ├── epic-oneshot.md
│   │   ├── standup.md
│   │   ├── blocked.md
│   │   ├── create_handoff.md
│   │   └── resume_handoff.md
│   └── agents/         # Specialized sub-agents
│       ├── codebase-locator.md
│       ├── codebase-analyzer.md
│       ├── codebase-pattern-finder.md
│       ├── web-search-researcher.md
│       ├── file-analyzer.md
│       ├── bug-hunter.md
│       └── test-runner.md
├── thoughts/           # RPI artifacts (symlinked to minty-thoughts)
│   ├── research/       # Research documents (OUTPUT from phase 1)
│   │   └── YYYY.MM.DD-username-description.md
│   ├── plans/          # Implementation plans (OUTPUT from phase 2)
│   │   └── YYYY.MM.DD-username-description.md
│   └── handoffs/       # Session handoff documents
│       └── YYYY.MM.DD-username-description.md
└── CLAUDE.md           # This file
```

## Critical Workflow: Context Resets Between Phases

**IMPORTANT**: Each phase should start with a fresh context window:

1. **Phase 1 (Research)**: Start fresh Claude session
   - Run: `/research How does authentication work?`
   - Output: `thoughts/research/2025.01.12-username-authentication.md`
   - Close/clear context

2. **Phase 2 (Planning)**: Start fresh Claude session
   - Run: `/plan thoughts/research/2025.01.12-username-authentication.md`
   - Output: `thoughts/plans/2025.01.12-username-oauth-support.md`
   - Close/clear context

3. **Phase 3 (Implementation)**: Start fresh Claude session
   - Run: `/implement thoughts/plans/2025.01.12-username-oauth-support.md`
   - Execute the plan with verification
   - Complete implementation

This intentional context reset prevents overflow and ensures each phase starts with exactly the information it needs.

## Document Formats

### Research Documents
- Located in `thoughts/research/` directory
- Symlinked to `~/dev/minty-thoughts/repos/[repo-name]/research/`
- Named: `YYYY.MM.DD-username-description.md`
- Include findings, code references, and insights
- Self-contained with all necessary context

### Implementation Plans
- Located in `thoughts/plans/` directory
- Symlinked to `~/dev/minty-thoughts/repos/[repo-name]/plans/`
- Named: `YYYY.MM.DD-username-description.md`
- Include phases, specific changes, and success criteria
- Separate automated and manual verification

### Handoff Documents
- Located in `thoughts/handoffs/` directory
- Symlinked to `~/dev/minty-thoughts/repos/[repo-name]/handoffs/`
- Named: `YYYY.MM.DD-username-description.md`
- Include task status, learnings, recent changes, and action items
- Enable context transfer between sessions

## Enhanced Capabilities

### File Analysis
The file-analyzer agent can reduce large log files and outputs by 80-90% while preserving critical information, making it invaluable for debugging production issues or analyzing verbose test outputs.

### Bug Detection
The bug-hunter agent provides elite-level bug detection, identifying security vulnerabilities, performance bottlenecks, and logic errors with specific remediation suggestions.

### Test Execution
The test-runner agent executes tests in an isolated context, preventing test output from polluting your main conversation while still providing actionable results.

### Project Management
- **Epic Oneshot**: Chain all three phases for quick feature implementation
- **Standup**: Generate daily progress reports automatically
- **Blocked**: Identify and resolve implementation impediments

## Best Practices

### During Research
- Read mentioned files FULLY before spawning sub-tasks
- Use parallel agents for efficiency
- Include specific file:line references
- Think deeply about architectural implications

### During Planning
- Be skeptical and thorough
- Work iteratively with the user
- No open questions in final plan
- Include "What we're NOT doing" section

### During Implementation
- Follow the plan's intent
- Adapt to reality when needed
- Verify continuously
- Update progress tracking

## Context Engineering Tips

1. **Research prevents bad code**
   - Misunderstanding = thousands of bad lines
   - Bad research = hundreds of bad lines
   - Bad plan = tens of bad lines

2. **Review markdown, not code**
   - Research files are easier to review than code
   - Plans show intent clearly
   - Catch problems before implementation

3. **Parallel processing**
   - Spawn multiple research agents simultaneously
   - Each agent focuses on specific aspects
   - Synthesize findings in main context

4. **Progress tracking**
   - Use TodoWrite for task management
   - Update plan checkboxes during implementation
   - Maintain clear status indicators

## Important Reminders

- **Always read files fully** - Never use limit/offset parameters
- **Wait for all agents** - Don't synthesize before agents complete
- **Verify continuously** - Run tests after each phase
- **Document deviations** - Note when reality differs from plan
- **Maintain quality** - No commented code, no TODOs

## Success Metrics

You know the workflow is working when:
- Research documents answer questions completely
- Plans are approved with minimal revisions
- Implementation proceeds without blocking issues
- Tests pass on first run
- Code follows existing patterns
- No back-and-forth corrections needed

## Getting Started

1. Start with `/research` to understand the codebase
2. Use `/plan` to create a detailed implementation plan
3. Execute with `/implement` following the plan
4. Iterate based on verification results

Remember: The goal is not just to write code, but to write the RIGHT code efficiently with minimal context usage and maximum correctness.