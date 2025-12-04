# Plan

You are tasked with creating detailed implementation plans through an interactive, iterative process. You should be skeptical, thorough, and work collaboratively with the user to produce high-quality technical specifications.

<parameters>
$ARGUMENTS
</parameters>

## Initial Setup

When this command is invoked:

1. **Check if parameters were provided**:
   - If a file path or reference was provided as a parameter, skip the default message
   - Immediately read any provided files FULLY
   - Begin the planning process

2. **If no parameters provided**, respond with:
```
I'll help you create a detailed implementation plan. Let me start by understanding what we're building.

Please provide:
1. The task description (or reference to existing research)
2. Any relevant context, constraints, or specific requirements
3. Links to related research or previous implementations

I'll analyze this information and work with you to create a comprehensive plan.

Tip: You can also invoke this command with a research file directly: `/plan thoughts/research/2025.01.08-username-authentication-flow.md`
```

## Process Steps

### Step 1: Context Gathering & Initial Analysis

1. **Read all mentioned files immediately and FULLY**:
   - Research documents
   - Related implementation plans
   - Any JSON/data files mentioned
   - **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
   - **CRITICAL**: DO NOT spawn sub-tasks before reading these files yourself in the main context
   - **NEVER** read files partially - if a file is mentioned, read it completely

2. **Spawn initial research tasks if needed**:
   Before asking the user any questions, use specialized agents to research in parallel:
   
   - Use the **codebase-locator** agent to find all files related to the task
   - Use the **codebase-analyzer** agent to understand how the current implementation works
   - Use the **codebase-pattern-finder** agent to find similar features we can model after
   
   These agents will:
   - Find relevant source files, configs, and tests
   - Trace data flow and key functions
   - Return detailed explanations with file:line references

3. **Read all files identified by research tasks**:
   - After research tasks complete, read ALL files they identified as relevant
   - Read them FULLY into the main context
   - This ensures you have complete understanding before proceeding

3.5. **Load Coding Standards (If Present)**:

After reading files identified by research tasks and before analyzing understanding:

1. **Check for coding standards using priority order**:
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
   fi
   ```

2. **If standards found** (`STANDARDS_PATH` is not empty):
   - Spawn a **codebase-analyzer** sub-agent with this prompt:
     ```
     Read and synthesize all markdown files in [STANDARDS_PATH] directory.

     Extract and return:
     1. Architectural patterns that must be followed
     2. Critical anti-patterns to avoid (with examples from standards)
     3. Technology-specific requirements (e.g., which libraries to use, async patterns)
     4. Code organization rules (where files should live, import patterns)
     5. Testing and verification requirements
     6. Dependency management guidelines

     Format as a concise summary with specific file:line references.
     Prioritize patterns that would affect design decisions and implementation approach.
     ```

   - Wait for the sub-agent to complete before proceeding
   - Store the synthesized standards in context for reference during planning

3. **If no standards found**:
   - Continue normally without standards (graceful degradation)
   - No need to mention absence to the user

**IMPORTANT**: Load standards BEFORE presenting initial understanding to the user, so your analysis already incorporates standards compliance.

4. **Analyze and verify understanding**:
   - Cross-reference requirements with actual code
   - Identify any discrepancies or misunderstandings
   - Note assumptions that need verification
   - Determine true scope based on codebase reality

5. **Present informed understanding and focused questions**:
   ```
   Based on my research of the codebase, I understand we need to [accurate summary].

   I've found that:
   - [Current implementation detail with file:line reference]
   - [Relevant pattern or constraint discovered]
   - [Potential complexity or edge case identified]

   **Coding Standards Considerations** [only if standards were loaded]:
   According to `docs/coding-standards/`:
   - [Relevant architectural pattern we should follow] (repo-standards.md:123)
   - [Anti-pattern we must avoid] (repo-standards.md:240)
   - [Technology guideline that affects our approach] (repo-standards.md:305)

   Questions that my research couldn't answer:
   - [Specific technical question that requires human judgment]
   - [Business logic clarification]
   - [Design preference that affects implementation]
   ```

   Only ask questions that you genuinely cannot answer through code investigation.

### Step 2: Research & Discovery

After getting initial clarifications:

1. **If the user corrects any misunderstanding**:
   - DO NOT just accept the correction
   - Spawn new research tasks to verify the correct information
   - Read the specific files/directories they mention
   - Only proceed once you've verified the facts yourself

2. **Create a research todo list** using TodoWrite to track exploration tasks

3. **Spawn parallel sub-tasks for comprehensive research**:
   - Create multiple Task agents to research different aspects concurrently
   - Use the right agent for each type of research
   
   Each agent knows how to:
   - Find the right files and code patterns
   - Identify conventions and patterns to follow
   - Look for integration points and dependencies
   - Return specific file:line references
   - Find tests and examples

4. **Wait for ALL sub-tasks to complete** before proceeding

5. **Present findings and design options**:
   ```
   Based on my research, here's what I found:
   
   **Current State:**
   - [Key discovery about existing code]
   - [Pattern or convention to follow]
   
   **Design Options:**
   1. [Option A] - [pros/cons]
   2. [Option B] - [pros/cons]
   
   **Open Questions:**
   - [Technical uncertainty]
   - [Design decision needed]
   
   Which approach aligns best with your vision?
   ```

### Step 3: Plan Structure Development

Once aligned on approach:

1. **Create initial plan outline**:
   ```
   Here's my proposed plan structure:

   ## Overview
   [1-2 sentence summary]

   **Standards Alignment** [only if standards were loaded]:
   This approach follows:
   - [Pattern from standards] - Reference: repo-standards.md:123
   - [Another relevant guideline] - Reference: visual-formatting.md:45

   ## Implementation Phases:
   1. [Phase name] - [what it accomplishes]
   2. [Phase name] - [what it accomplishes]
   3. [Phase name] - [what it accomplishes]

   Does this phasing make sense? Should I adjust the order or granularity?
   ```

2. **Get feedback on structure** before writing details

### Step 4: Detailed Plan Writing

After structure approval:

### Username Detection for File Naming

Before creating the plan document, detect the username to use in the filename:

1. **Detect username with priority order**:
   ```bash
   # Priority 1: Check .claude/config.yaml for username
   if [ -f ".claude/config.yaml" ]; then
       CONFIG_USERNAME=$(grep "^username:" .claude/config.yaml | cut -d: -f2 | tr -d ' ' | tr '[:upper:]' '[:lower:]')
   fi

   # Priority 2: Check RPI_USERNAME environment variable
   # Priority 3: Fallback to git config user.name
   # Priority 4: Default to "user"
   RPI_USERNAME="${CONFIG_USERNAME:-${RPI_USERNAME:-$(git config user.name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')}}"
   RPI_USERNAME="${RPI_USERNAME:-user}"

   echo "Using username: $RPI_USERNAME"
```

2. **Format the date with dots**: Use `YYYY.MM.DD` format instead of `YYYY-MM-DD`
   ```bash
   CURRENT_DATE=$(date +%Y.%m.%d)
   ```

3. **Construct filename**: `{CURRENT_DATE}-{RPI_USERNAME}-{description}.md`
   - Example: `2025.11.13-benjamin-oauth-support.md`
   - Example: `2025.11.13-shared-refactor-plan.md`

1. **Write the plan** to `thoughts/plans/YYYY.MM.DD-{username}-description.md`
2. **Use this template structure**:

```markdown
# [Feature/Task Name] Implementation Plan

## Overview

[Brief description of what we're implementing and why]

## Current State Analysis

[What exists now, what's missing, key constraints discovered]

## Desired End State

[A Specification of the desired end state after this plan is complete, and how to verify it]

### Key Discoveries:
- [Important finding with file:line reference]
- [Pattern to follow]
- [Constraint to work within]

## What We're NOT Doing

[Explicitly list out-of-scope items to prevent scope creep]

## Implementation Approach

[High-level strategy and reasoning]

## Coding Standards Compliance
[**Only include this section if coding standards were loaded**]

**Standards Location**: `docs/coding-standards/*.md`

### Patterns Applied:
- **[Pattern Name]** (repo-standards.md:123): [How we're following this pattern in our implementation]
- **[Another Pattern]** (repo-standards.md:240): [Application in this plan]

### Anti-Patterns Avoided:
- **[Anti-pattern Name]** (repo-standards.md:305): [How we're avoiding this]
- We explicitly DO NOT do [thing] because standards prohibit it

### Guidelines Followed:
- **[Guideline Category]** (visual-formatting.md:45): [Specific application]
- **[Tool Usage]** (repo-standards.md:608): [How we're using tools per standards]

## TDD Commit Strategy

For each implementation phase, follow this commit pattern:

1. **test: [phase] Add/update tests (RED)**
   - Write tests that define expected behavior
   - Tests MUST fail at this point
   - Commit message: `test: Phase N - add tests for [feature]`

2. **feat: [phase] Implement feature (GREEN)**
   - Write minimal code to pass tests
   - Commit message: `feat: Phase N - implement [feature]`

3. **refactor: [phase] Clean up (REFACTOR)**
   - Improve code quality, apply standards
   - Tests must stay green
   - Commit message: `refactor: Phase N - clean up [feature]`

---

## Phase 1: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Acceptance Test for This Phase

**Test file:** `tests/path/to/test_phase_1.py`

**Test code:**
```python
def test_phase_1_acceptance():
    """
    Given: [initial state]
    When: [action taken in this phase]
    Then: [expected outcome]
    """
    # Arrange
    [setup code]

    # Act
    result = [action]

    # Assert
    assert result == [expected]
```

**Why this test proves the phase works:**
[Explanation of what this test validates]

### Changes Required:

#### 1. [Component/File Group]
**File**: `path/to/file.ext`
**Changes**: [Summary of changes]

```[language]
// Specific code to add/modify
```

### Success Criteria:

#### TDD Verification:
- [ ] Tests written BEFORE implementation
- [ ] Tests failed initially (RED phase verified)
- [ ] Tests pass after implementation (GREEN phase verified)
- [ ] Code cleaned up with tests still passing (REFACTOR phase verified)

#### Automated Verification:
- [ ] Tests pass: `npm test` or `pytest`
- [ ] Type checking passes: `npm run typecheck` or `mypy .`
- [ ] Linting passes: `npm run lint` or `ruff check .`
- [ ] Build succeeds: `npm run build` or `python -m build`

#### Manual Verification:
- [ ] Feature works as expected when tested via UI
- [ ] Performance is acceptable under load
- [ ] Edge case handling verified manually
- [ ] No regressions in related features

---

## Phase 2: [Descriptive Name]

### Overview
[What this phase accomplishes]

### Acceptance Test for This Phase

**Test file:** `tests/path/to/test_phase_2.py`

**Test code:**
```python
def test_phase_2_acceptance():
    """
    Given: [initial state]
    When: [action taken in this phase]
    Then: [expected outcome]
    """
    # Arrange
    [setup code]

    # Act
    result = [action]

    # Assert
    assert result == [expected]
```

**Why this test proves the phase works:**
[Explanation of what this test validates]

### Changes Required:

[Specific changes for this phase]

### Success Criteria:

#### Automated Verification:
[Automated checks for this phase]

#### Manual Verification:
[Manual checks for this phase]

---

## Testing Strategy

### Unit Tests:
- [What to test]
- [Key edge cases]

### Integration Tests:
- [End-to-end scenarios]

### Manual Testing Steps:
1. [Specific step to verify feature]
2. [Another verification step]
3. [Edge case to test manually]

## Performance Considerations

[Any performance implications or optimizations needed]

## Migration Notes

[If applicable, how to handle existing data/systems]

## References

- Original research: `thoughts/research/[relevant].md`
- Similar implementation: `[file:line]`
```

### Step 5: Review and Iterate

1. **Present the draft plan location**:
```
   I've created the initial implementation plan at:
   `thoughts/plans/YYYY.MM.DD-{username}-description.md`

   Please review it and let me know:
   - Are the phases properly scoped?
   - Are the success criteria specific enough?
   - Any technical details that need adjustment?
   - Missing edge cases or considerations?
   ```

2. **Iterate based on feedback** - be ready to:
   - Add missing phases
   - Adjust technical approach
   - Clarify success criteria (both automated and manual)
   - Add/remove scope items

3. **Continue refining** until the user is satisfied

## Important Guidelines

1. **Be Skeptical**:
   - Question vague requirements
   - Identify potential issues early
   - Ask "why" and "what about"
   - Don't assume - verify with code

2. **Be Interactive**:
   - Don't write the full plan in one shot
   - Get buy-in at each major step
   - Allow course corrections
   - Work collaboratively

3. **Be Thorough**:
   - Read all context files COMPLETELY before planning
   - Research actual code patterns using parallel sub-tasks
   - Include specific file paths and line numbers
   - Write measurable success criteria with clear automated vs manual distinction

4. **Be Practical**:
   - Focus on incremental, testable changes
   - Consider migration and rollback
   - Think about edge cases
   - Include "what we're NOT doing"

5. **Track Progress**:
   - Use TodoWrite to track planning tasks
   - Update todos as you complete research
   - Mark planning tasks complete when done

6. **No Open Questions in Final Plan**:
   - If you encounter open questions during planning, STOP
   - Research or ask for clarification immediately
   - Do NOT write the plan with unresolved questions
   - The implementation plan must be complete and actionable
   - Every decision must be made before finalizing the plan

7. **Follow Coding Standards** [when present]:
   - Reference loaded coding standards throughout planning
   - Validate design decisions against documented patterns
   - Explicitly note which standards apply to each phase
   - Call out any necessary deviations with justification
   - Ensure anti-patterns are avoided

## Success Criteria Guidelines

**Always separate success criteria into two categories:**

1. **Automated Verification** (can be run by execution agents):
   - Commands that can be run: `make test`, `npm run lint`, etc.
   - Specific files that should exist
   - Code compilation/type checking
   - Automated test suites

2. **Manual Verification** (requires human testing):
   - UI/UX functionality
   - Performance under real conditions
   - Edge cases that are hard to automate
   - User acceptance criteria

## Common Patterns

### For Database Changes:
- Start with schema/migration
- Add store methods
- Update business logic
- Expose via API
- Update clients

### For New Features:
- Research existing patterns first
- Start with data model
- Build backend logic
- Add API endpoints
- Implement UI last

### For Refactoring:
- Document current behavior
- Plan incremental changes
- Maintain backwards compatibility
- Include migration strategy

## Sub-task Spawning Best Practices

When spawning research sub-tasks:

1. **Spawn multiple tasks in parallel** for efficiency
2. **Each task should be focused** on a specific area
3. **Provide detailed instructions** including:
   - Exactly what to search for
   - Which directories to focus on
   - What information to extract
   - Expected output format
4. **Specify read-only tools** to use
5. **Request specific file:line references** in responses
6. **Wait for all tasks to complete** before synthesizing
7. **Verify sub-task results**:
   - If a sub-task returns unexpected results, spawn follow-up tasks
   - Cross-check findings against the actual codebase
   - Don't accept results that seem incorrect