# Blocked

Identifies and analyzes implementation blockers, dependencies, and impediments.

## Initial Response

When this command is invoked, respond with:
```
I'll analyze your current work to identify blockers and suggest resolutions. Let me examine your plans, code, and dependencies...
```

## Process Steps

### Step 1: Identify Potential Blockers

1. **Scan active plans**:
   - Read plans in `thoughts/plans/` directory
   - Look for incomplete phases
   - Check success criteria not met
   - Identify dependencies

2. **Check implementation state**:
   ```bash
   # For Python projects:
   if [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
       # Check for failing tests
       pytest 2>&1 | grep -E "(FAILED|ERROR|ERRORS)"

       # Check for type errors
       mypy . 2>&1 | grep -E "error:|Error"

       # Check for lint issues
       ruff check . 2>&1 | grep -E "error|Error" || flake8 . 2>&1 | grep -E "E[0-9]"

       # Check import sorting
       isort . --check-only 2>&1 | grep -E "ERROR"
   fi

   # For JavaScript/TypeScript projects:
   if [ -f "package.json" ]; then
       # Check for failing tests
       npm test 2>&1 | grep -E "(FAIL|Error|✗)"

       # Check for type errors
       npm run typecheck 2>&1 | grep -E "error|Error"

       # Check for lint issues
       npm run lint 2>&1 | grep -E "error|Error"

       # Check build status
       npm run build 2>&1 | grep -E "error|failed|Error"
   fi
   ```

3. **Analyze code for blockers**:
   - Search for TODO/FIXME/HACK/XXX comments
   - Look for `throw new Error("Not implemented")`
   - Find commented out code blocks
   - Identify missing dependencies

4. **Check external dependencies**:
   ```bash
   # For Python projects:
   if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
       # Check for missing packages
       pip check 2>&1 | grep -E "not installed|No matching"

       # Check for outdated packages
       pip list --outdated

       # Check for security issues
       pip-audit || safety check
   fi

   # For JavaScript/TypeScript projects:
   if [ -f "package.json" ]; then
       # Check for missing packages
       npm ls 2>&1 | grep "UNMET"

       # Check for outdated critical deps
       npm outdated

       # Check for security issues
       npm audit --audit-level=moderate
   fi
   ```

### Step 2: Categorize Blockers

Organize findings by type:

```markdown
# Blocker Analysis Report

## 🚫 Critical Blockers (Preventing Progress)

### 1. [Blocker Name]
- **Type**: [Technical/Dependency/Knowledge/Access]
- **Location**: `file:line` or `plan:phase`
- **Impact**: [What can't proceed]
- **Details**: [Specific error or issue]
- **Resolution Options**:
  1. [Preferred solution]
  2. [Alternative approach]
  3. [Workaround if applicable]
- **Time Estimate**: [Hours/Days to resolve]
- **Needs**: [What's required - access/info/decision]

## ⚠️ Partial Blockers (Slowing Progress)

### 1. [Issue Name]
- **Impact**: [What's affected]
- **Current Workaround**: [If any]
- **Permanent Fix**: [What's needed]
- **Priority**: [High/Medium/Low]

## 🔄 Dependency Issues

### Waiting On:
- [ ] [External dependency or decision]
  - Who: [Person/Team]
  - Needed by: [Date/Phase]
  - Impact if delayed: [Consequence]

### Missing Information:
- [ ] [Required documentation/spec]
  - Where to find: [Potential source]
  - Alternative: [Other approach]

## 💭 Knowledge Gaps

### Need Clarification:
1. **[Technical Question]**
   - Context: [Why this matters]
   - Options considered: [What was tried]
   - Recommendation: [Best guess]

## 📊 Blocker Statistics
- **Total Blockers**: X
- **Critical**: Y
- **Resolved Today**: Z
- **Age of Oldest**: N days
```

### Step 3: Provide Resolution Path

```markdown
## 🎯 Recommended Action Plan

### Immediate Actions (Do Now):
1. [Specific step to unblock critical item]
   ```bash
   [Command if applicable]
   ```
2. [Communication needed]
   - Send message to: [Person]
   - Ask: [Specific question]

### Short-term Solutions (Today):
- [Workaround to maintain momentum]
- [Alternative approach to try]

### Long-term Fixes (This Week):
- [Proper solution to implement]
- [Process improvement needed]

## 🔧 Unblocking Commands

Based on the blockers found, here are commands that might help:

```bash
# For Python projects:
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    # Fix missing dependencies
    pip install -r requirements.txt
    # or for pyproject.toml:
    pip install -e .

    # Clear caches if needed
    pip cache purge
    rm -rf __pycache__ .pytest_cache .mypy_cache
    find . -type d -name "*.egg-info" -exec rm -rf {} +

    # Reset test environment
    pytest --cache-clear

    # Reinstall in development mode
    pip install -e ".[dev]"
fi

# For JavaScript/TypeScript projects:
if [ -f "package.json" ]; then
    # Fix missing dependencies
    npm install

    # Clear caches if needed
    npm cache clean --force
    rm -rf node_modules package-lock.json
    npm install

    # Reset test environment
    npm test -- --clearCache
fi

# Check environment variables (both Python and JS)
env | grep -E "(API|KEY|TOKEN|URL|PYTHON|NODE|DATABASE)"
```

## 📈 Progress Despite Blockers

Here's what CAN continue while blocked:
1. [Task that's not dependent]
2. [Documentation that can be written]
3. [Tests that can be added]
4. [Refactoring opportunity]
```

### Step 4: Track and Update

If blockers were previously identified:
```
## 📊 Blocker Trend
- **New Blockers**: +X
- **Resolved Since Last Check**: Y
- **Still Blocked**: Z
- **Average Resolution Time**: N hours

Previously tracked blockers:
- ✅ [Resolved]: [How it was fixed]
- 🔄 [Still active]: [Status update]
- 🆕 [New]: [Just discovered]
```

## Analysis Techniques

### Code Scanning Patterns
```bash
# Find all TODO/FIXME comments
grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.js"

# Find not implemented functions
grep -r "throw.*Error.*[Nn]ot.*implemented" --include="*.ts"

# Find commented code blocks
grep -r "^[[:space:]]*//.*{$" --include="*.ts"

# Find typescript errors
grep -r "@ts-ignore\|@ts-expect-error" --include="*.ts"
```

### Dependency Analysis
- Check package.json for missing scripts
- Verify required environment variables
- Check for circular dependencies
- Identify version conflicts

### Plan Analysis
- Look for phases marked incomplete
- Check dependencies between phases
- Identify prerequisites not met
- Find success criteria failing

## Important Guidelines

- **Be specific** about what's blocking
- **Provide actionable solutions** not just problems
- **Prioritize by impact** on current work
- **Include time estimates** for resolution
- **Track resolution** of previous blockers
- **Suggest workarounds** where possible

## Integration with Other Commands

Can be called by:
- `/implement` when hitting issues
- `/standup` to report impediments
- `/plan` to identify risks early

Remember: The goal is not just to identify blockers but to provide clear paths to resolution and maintain development momentum.