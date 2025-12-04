# Standup

Generates a comprehensive status report from recent RPI artifacts and git activity.

## Initial Response

When this command is invoked, respond with:
```
I'll generate a standup report from your recent work. Let me analyze your RPI artifacts and git history...
```

## Process Steps

### Step 1: Gather Information

1. **Check git status and history**:
   ```bash
   # Get recent commits
   git log --oneline -10

   # Check current branch
   git branch --show-current

   # Check uncommitted changes
   git status --short
   ```

2. **Scan RPI artifacts**:
   - List recent files in `thoughts/research/` directory
   - List recent files in `thoughts/plans/` directory
   - Check for in-progress implementations

3. **Analyze todos**:
   - Check for any active TodoWrite items
   - Look for TODO/FIXME comments in changed files

### Step 2: Generate Report

Create a structured standup report:

```markdown
# Daily Standup - [Date]

## 📊 Current Status
- **Branch**: [branch-name]
- **Last Commit**: [time ago] - [commit message]
- **Uncommitted Changes**: [X files]

## ✅ Recently Completed
[Based on recent commits and completed plans]
- [Task/Feature 1] - [Brief description]
  - Files affected: X
  - Tests: ✅ Passing
- [Task/Feature 2] - [Brief description]

## 🚧 In Progress
[Based on uncommitted changes and active plans]
- [Current task] ([X]% complete)
  - Plan: thoughts/plans/[filename].md
  - Next step: [Description]

## 📋 Upcoming
[Based on pending plans and TODOs]
1. [Next priority task]
2. [Following task]
3. [Future consideration]

## 🔬 Recent Research
[From thoughts/research/ directory]
- [Topic] - thoughts/research/[filename].md
  - Key finding: [Brief summary]

## ⚠️ Blockers/Issues
[From blocked items or errors]
- [Issue description] - [What's needed to resolve]

## 📈 Metrics
- **Commits Today**: X
- **Files Changed**: Y
- **Test Coverage**: Z%
- **Active Plans**: N

## 🎯 Today's Focus
Based on current progress, the priorities are:
1. [Primary focus]
2. [Secondary task]
3. [If time permits]
```

### Step 3: Provide Actionable Summary

```
Standup generated! Here's your executive summary:

**Momentum**: [Good/Blocked/Slow]
**Key Achievement**: [Most important recent completion]
**Main Focus**: [What you should work on next]
**Needs Attention**: [Any blockers or issues]

Would you like me to:
1. Share this in a specific format (Slack, email, etc.)?
2. Create action items from blockers?
3. Prioritize the upcoming work?
```

## Data Sources

### Git Information
- Recent commits (last 24-48 hours)
- Current branch and upstream status
- Uncommitted changes
- Stash status

### RPI Artifacts
- Files modified in last 3 days
- Research documents created
- Plans in various states
- Implementation progress

### Code Analysis
- TODO/FIXME comments
- Test results if available
- Coverage reports if available
- Lint status

## Customization Options

If user provides parameters:
- `--days N` - Look back N days (default: 1)
- `--verbose` - Include more detail
- `--metrics` - Focus on quantitative data
- `--blockers` - Emphasize blockers/issues

## Important Guidelines

- **Be concise** - Standups should be scannable
- **Be honest** - Don't hide blockers
- **Be specific** - Use real file names and numbers
- **Be actionable** - Identify clear next steps
- **Be informative** - Provide context for decisions

## Output Formats

Can adapt output for different needs:
- **Slack**: Emoji-rich, formatted for channels
- **Email**: Professional, detailed
- **Terminal**: Concise, command-line friendly
- **Markdown**: Full detail for documentation

Remember: The standup should give a clear picture of progress, current state, and what's next.