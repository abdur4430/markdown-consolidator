# Implement

You are tasked with implementing an approved technical plan. These plans contain phases with specific changes and success criteria.

<plan_path>
$ARGUMENTS
</plan_path>

## Getting Started

When given a plan path:
- Read the plan completely and check for any existing checkmarks (- [x])
- Read any original research documents mentioned in the plan
- **Read files fully** - never use limit/offset parameters, you need complete context
- **Load coding standards if present**:
  - Check for standards using this priority order:
    ```bash
    # Priority 1: External standards via MINTY_DOCS_PATH environment variable
    if [ -n "$MINTY_DOCS_PATH" ] && [ -d "$MINTY_DOCS_PATH/cross-cutting/coding-standards/" ]; then
        STANDARDS_PATH="$MINTY_DOCS_PATH/cross-cutting/coding-standards/"
        echo "Found external coding standards (via MINTY_DOCS_PATH)"
    # Priority 2: Local repository standards
    elif [ -d "docs/coding-standards/" ]; then
        STANDARDS_PATH="docs/coding-standards/"
        echo "Found local coding standards"
    else
        STANDARDS_PATH=""
        echo "No coding standards found - continuing without standards"
    fi
    ```
  - If standards found (`STANDARDS_PATH` is not empty), spawn a **codebase-analyzer** sub-agent:
    ```
    Read and synthesize all markdown files in [STANDARDS_PATH] directory.

    Extract and return:
    1. Code organization patterns (file placement, package structure)
    2. Anti-patterns to avoid during implementation
    3. Code style and formatting requirements
    4. Import patterns and dependency usage rules
    5. Testing requirements and patterns
    6. Common implementation gotchas from standards

    Format as actionable implementation checklist with specific file:line references.
    Focus on patterns that affect how code should be written and organized.
    ```
  - Wait for synthesis to complete before starting implementation
  - Keep standards in context for reference during implementation
  - If no standards found, continue normally (graceful degradation - NO error, NO user notification)
- **Invoke TDD Skill (if available)**:
  - Check if `superpowers:test-driven-development` skill is available
  - If available, use the Skill tool to invoke it
  - This skill enforces the RED-GREEN-REFACTOR cycle:
    1. **RED**: Write/update tests FIRST - they MUST fail initially
    2. **GREEN**: Write minimal code to make tests pass
    3. **REFACTOR**: Clean up while keeping tests green
  - If TDD skill is not available, follow the TDD workflow manually as described in "Make the Changes" section
  - TDD is strongly recommended for all implementation work
- Think deeply about how the pieces fit together
- Create a todo list to track your progress
- Start implementing if you understand what needs to be done

If no plan path provided, ask for one.

## Implementation Philosophy

Plans are carefully designed, but reality can be messy. Your job is to:
- Follow the plan's intent while adapting to what you find
- **Adhere to coding standards** (if present) for all new/modified code
- Implement each phase fully before moving to the next
- Verify your work makes sense in the broader codebase context
- Update checkboxes in the plan as you complete sections
- **Reference standards when making decisions** about code organization, patterns, and style

When things don't match the plan exactly, think about why and communicate clearly. The plan is your guide, but your judgment matters too.

**When standards exist and affect implementation**:
- Follow documented patterns for code organization
- Avoid documented anti-patterns
- Apply required code style and formatting rules
- Use specified tools and dependencies as documented
- Reference specific standards in commit messages when applicable

If you encounter a mismatch:
- STOP and think deeply about why the plan can't be followed
- Present the issue clearly:
  ```
  Issue in Phase [N]:
  Expected: [what the plan says]
  Found: [actual situation]
  Why this matters: [explanation]
  
  How should I proceed?
  ```

## Implementation Process

### Step 1: Preparation
1. Read the entire plan to understand the full scope
2. Note any phases already marked complete
3. Read all files mentioned in the plan FULLY
4. Create a TodoWrite list with:
   - One item for each phase
   - Sub-items for major changes within each phase
   - Items for verification steps

### Step 2: Phase-by-Phase Implementation
For each phase:

1. **Understand the Goal**
   - Re-read the phase overview
   - Understand what this phase accomplishes
   - Review the success criteria

2. **Make the Changes (TDD Workflow)**
   - **For each feature/change in the phase**:
     1. **RED Phase**: Write or update tests FIRST
        - Run tests to confirm they FAIL
        - If tests pass before implementation, the tests are not testing the new behavior
        - Commit: `test: Phase N - add tests for [feature]`
     2. **GREEN Phase**: Write minimal implementation
        - Only write code needed to make tests pass
        - Resist adding features not covered by tests
        - Commit: `feat: Phase N - implement [feature]`
     3. **REFACTOR Phase**: Clean up
        - Improve code quality while keeping tests green
        - Apply coding standards (if loaded)
        - Commit: `refactor: Phase N - clean up [feature]`
   - Follow the code examples from the plan closely
   - **Apply coding standards** (if loaded) to all new/modified code:
     - Place files in correct locations per standards
     - Use documented import patterns
     - Follow established architectural patterns
     - Avoid documented anti-patterns
     - Apply required code style/formatting
   - Adapt to actual code structure as needed

3. **Verify as You Go**
   - Run automated verification commands after each major change
   - Fix issues immediately before proceeding
   - Don't accumulate technical debt

4. **Update Progress**
   - Check off completed items in the plan using Edit
   - Update your TodoWrite list
   - Note any deviations from the plan

### Step 3: Verification Approach

After implementing a phase:
- Run all automated success criteria checks
- Usually `make check test` or similar covers everything
- Fix any issues before proceeding
- Update your progress in both the plan and your todos
- Check off completed items in the plan file itself using Edit

Don't let verification interrupt your flow - batch it at natural stopping points.

### Step 4: Phase Completion

Before moving to the next phase:
1. Ensure all automated verification passes
2. Update the plan with checkmarks for completed items
3. Document any significant deviations
4. Commit your changes if appropriate

### Step 5: Documentation Update

After all implementation phases complete and verification passes, consider whether documentation updates are needed.

1. **Determine if documentation is warranted**:
   - Was a new feature or capability added?
   - Were existing behaviors significantly changed?
   - Were new patterns introduced that others should follow?
   - Were anti-patterns discovered and resolved?

   If no documentation is needed, skip to Git Commit Best Practices.

2. **Classify documentation type**:
   ```bash
   # Check what documentation destinations are available
   DOCS_DESTINATION=""
   DOCS_TYPE=""

   # Priority 1: Cross-cutting documentation (affects multiple repos)
   if [ -n "$MINTY_DOCS_PATH" ] && [ -d "$MINTY_DOCS_PATH" ]; then
       echo "Cross-cutting docs available at: $MINTY_DOCS_PATH"
       CROSS_CUTTING_AVAILABLE="true"
   else
       CROSS_CUTTING_AVAILABLE="false"
   fi

   # Priority 2: Repo-specific documentation
   if [ -d "docs/" ]; then
       echo "Repo-specific docs available at: docs/"
       REPO_DOCS_AVAILABLE="true"
   else
       REPO_DOCS_AVAILABLE="false"
   fi

   # If neither exists, skip documentation silently
   if [ "$CROSS_CUTTING_AVAILABLE" = "false" ] && [ "$REPO_DOCS_AVAILABLE" = "false" ]; then
       echo "No documentation destinations configured - skipping documentation update"
   fi
   ```

3. **Determine appropriate destination**:
   - **Cross-cutting** (`$MINTY_DOCS_PATH/cross-cutting/`): Use for patterns, standards, or behaviors that affect multiple repositories
   - **Repo-specific** (`docs/`): Use for features, APIs, or behaviors specific to this repository

4. **Create or update documentation**:
   - Follow existing documentation structure in the destination
   - Include relevant code references from this implementation
   - Link back to the implementation plan if applicable

5. **Graceful degradation**:
   - If the appropriate destination doesn't exist, log what would have been documented
   - Continue with git commit - missing docs destination is NOT a blocker
   - User can manually create documentation later if needed

## Git Commit Best Practices

During implementation, maintain clean git history with atomic commits:

### Setup Before Implementation
```bash
# Save initial state
git status --porcelain > /tmp/rpi_baseline
export IMPL_START=$(git rev-parse HEAD)
echo "Implementation starting from commit: $IMPL_START"

# Detect project type for later verification
if [ -f "package.json" ]; then
    export PROJECT_TYPE="javascript"
    echo "Detected JavaScript/TypeScript project"
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
    export PROJECT_TYPE="python"
    echo "Detected Python project"
else
    export PROJECT_TYPE="unknown"
    echo "Project type not detected, will try both verification methods"
fi
```

### During Each Phase

Track and commit phase-specific changes:

```bash
# After completing a phase, stage only phase files
git diff --name-only $IMPL_START > /tmp/phase_changes

# Review what will be staged
echo "Files modified in this phase:"
cat /tmp/phase_changes

# Stage phase files selectively
for file in $(cat /tmp/phase_changes); do
    if [ -f "$file" ]; then
        git add "$file"
    fi
done

# Commit with descriptive message
git commit -m "Phase [N]: [Phase Title]

- [Brief description of changes]
- [Key files modified]

Implementation from: thoughts/plans/[plan-file].md
Phase [N] of [Total]: [Percentage]% complete"
```

### Selective Staging Patterns

For different types of changes:

```bash
# Python projects:
if [ "$PROJECT_TYPE" = "python" ]; then
    # Stage only source code changes
    git add **/*.py --ignore-errors
    git add src/**/*.py tests/**/*.py --ignore-errors

    # Stage only test changes
    git add test_*.py *_test.py tests/**/*.py --ignore-errors

    # Stage configuration changes
    git add pyproject.toml setup.py setup.cfg requirements*.txt .flake8 .ruff.toml --ignore-errors
fi

# JavaScript/TypeScript projects:
if [ "$PROJECT_TYPE" = "javascript" ]; then
    # Stage only source code changes
    git add src/**/*.{ts,js,tsx,jsx} --ignore-errors

    # Stage only test changes
    git add **/*.test.{ts,js} **/*.spec.{ts,js} --ignore-errors

    # Stage configuration changes
    git add package.json tsconfig.json .eslintrc --ignore-errors
fi

# Stage only documentation (both types)
git add **/*.md docs/** README.* --ignore-errors
```

### After Implementation

Verify clean state and run final checks:

```bash
# Run project-appropriate verification
if [ "$PROJECT_TYPE" = "python" ]; then
    echo "Running Python verification..."
    pytest --tb=short || echo "⚠️ Some tests failed"
    ruff check . || flake8 . || echo "⚠️ Linting issues found"
    mypy . --ignore-missing-imports || echo "⚠️ Type issues found"
elif [ "$PROJECT_TYPE" = "javascript" ]; then
    echo "Running JavaScript/TypeScript verification..."
    npm test || echo "⚠️ Some tests failed"
    npm run lint || echo "⚠️ Linting issues found"
    npm run typecheck || echo "⚠️ Type issues found"
fi

# Check final git status
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ Working directory clean - all changes committed"
    echo "Commits created during implementation:"
    git log --oneline $IMPL_START..HEAD
else
    echo "⚠️ Uncommitted changes remain:"
    git status --short
    echo "Consider:"
    echo "  - git add -p  # Interactive staging"
    echo "  - git stash   # Save for later"
fi
```

### Commit Message Templates

Use structured messages for clarity:

```bash
# Feature implementation
git commit -m "feat: Add [feature name]

- Implement [component/function]
- Add tests for [functionality]
- Update documentation

Closes: #[issue]
Plan: thoughts/plans/YYYY.MM.DD-username-feature.md"

# Bug fix
git commit -m "fix: Resolve [issue description]

- Root cause: [explanation]
- Solution: [what was changed]
- Tests added to prevent regression

Fixes: #[issue]"

# Refactoring
git commit -m "refactor: Improve [component/area]

- Extract [functionality] to [location]
- Reduce complexity from X to Y
- No functional changes

Part of: thoughts/plans/YYYY.MM.DD-username-refactor.md"
```

### Important Git Guidelines

- **Commit early and often** - Each phase should have its own commit
- **Keep commits atomic** - One logical change per commit
- **Write clear messages** - Future you will thank present you
- **Reference plans** - Link commits to implementation plans
- **Don't commit broken code** - Each commit should pass tests
- **Use conventional commits** - feat:, fix:, refactor:, docs:, test:

## Handling Issues

### When Tests Fail
1. Read the error message carefully
2. Understand what the test expects
3. Fix the implementation, not the test (unless the test is wrong)
4. Re-run verification

### When the Plan Doesn't Match Reality
1. Determine if the codebase has changed since planning
2. Assess if the plan's intent can still be achieved
3. Present the mismatch clearly to the user
4. Propose an adaptation that maintains the plan's goals

### When You Need More Context
Use sub-agents sparingly for:
- Targeted debugging of specific issues
- Exploring unfamiliar parts of the codebase
- Finding examples of similar implementations

## Progress Tracking

Maintain clear progress indicators:
- Use TodoWrite to track implementation tasks
- Update plan checkboxes as you complete sections
- Provide periodic status updates for long implementations
- Note any blockers or concerns immediately

## If You Get Stuck

When something isn't working as expected:
- First, make sure you've read and understood all the relevant code
- Consider if the codebase has evolved since the plan was written
- Present the mismatch clearly and ask for guidance
- Don't waste time on approaches that clearly won't work

## Resuming Work

If the plan has existing checkmarks:
- Trust that completed work is done
- Pick up from the first unchecked item
- Verify previous work only if something seems off
- Don't re-implement completed phases

## Implementation Best Practices

1. **Follow the Plan's Structure**
   - Implement phases in order
   - Complete each phase fully before moving on
   - Don't jump ahead even if you see the solution

2. **Maintain Code Quality**
   - **Follow coding standards** (if present) for all code changes
     - Reference specific standards in commit messages: "Follows pattern from repo-standards.md:123"
     - Avoid anti-patterns documented in standards
   - Follow existing code patterns (and documented standards patterns take precedence)
   - Keep consistent style
   - Add appropriate error handling
   - Don't introduce new dependencies without approval (check dependency management standards)

3. **Test Continuously**
   - Run tests after each significant change
   - Don't accumulate failing tests
   - Fix breaks immediately

4. **Communicate Progress**
   - Update todos regularly
   - Check off plan items as completed
   - Report blockers immediately
   - Note any concerns or uncertainties

## Success Indicators

You know you're doing well when:
- Tests pass after each phase
- The code follows existing patterns
- You're making steady progress through the plan
- You catch issues early and fix them
- The implementation matches the plan's intent

## Common Pitfalls to Avoid

- Don't skip reading files fully
- Don't assume the plan is perfect - adapt as needed
- Don't accumulate technical debt
- Don't implement multiple phases without verification
- Don't ignore failing tests
- Don't make changes outside the plan's scope

## Final Checklist

Before declaring implementation complete:
- [ ] All phases implemented
- [ ] All automated verification passing
- [ ] **Coding standards followed** (if present - spot check 2-3 changes against standards)
- [ ] Plan updated with completion checkmarks
- [ ] Any deviations documented
- [ ] Code follows project conventions
- [ ] No commented-out code or TODOs left
- [ ] All tests passing
- [ ] **Documentation considered** (new feature? → update docs/ or $MINTY_DOCS_PATH)

Remember: You're implementing a solution, not just checking boxes. Keep the end goal in mind and maintain forward momentum.