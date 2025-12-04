# Research

You are tasked with conducting comprehensive research across the codebase to answer user questions by spawning parallel sub-agents and synthesizing their findings.

<research_query>
$ARGUMENTS
</research_query>

## Initial Setup

When this command is invoked:

1. **Check if a research query was provided**:
   - If a query was provided as a parameter, skip the default message
   - Immediately proceed to Step 1 with the provided query
   - Begin the research process

2. **If no query provided**, respond with:
```
I'm ready to research the codebase. Please provide your research question or area of interest, and I'll analyze it thoroughly by exploring relevant components and connections.
```

Then wait for the user's research query.

## Process Steps

### Step 1: Read Directly Mentioned Files
- If the user mentions specific files (tickets, docs, JSON), read them FULLY first
- **IMPORTANT**: Use the Read tool WITHOUT limit/offset parameters to read entire files
- **CRITICAL**: Read these files yourself in the main context before spawning any sub-tasks
- This ensures you have full context before decomposing the research

### Step 1.25: Pre-Research Clarifying Questions

Before spawning agents, ask **minimal clarifying questions** to ensure you understand what to research:

**IMPORTANT**:
- Ask questions **ONE AT A TIME** (serial, not parallel)
- Prefer **multiple choice** when possible
- Focus on **MINIMAL information needed**, not exhaustive discovery
- Only ask 2-4 questions maximum
- Goal: Ensure agents research the RIGHT thing, not everything

**Question Framework** (adapt to context, don't ask all):

1. **Feature Type**:
   - "What type of work is this? (A) New feature, (B) Bug fix, (C) Refactoring, (D) Investigation"

2. **Expected Scope** (if unclear from initial query):
   - "Which repos do you expect this to touch? (A) Single repo: [name], (B) Multiple repos: [list], (C) Unknown - please investigate"

3. **Integration Concerns** (if feature spans repos):
   - "Does this feature involve: (A) API calls between services, (B) Shared data models, (C) Database changes, (D) All of the above, (E) None - isolated feature"

4. **Acceptance Criteria** (if not provided):
   - "How will we know this works? (A) Specific test passes, (B) User can perform action X, (C) System behaves as Y, (D) Not sure - help me define this"

**When to Skip Questions**:
- User provided a detailed research document or spec → Skip, read the doc
- Query is clearly scoped investigation ("How does X work?") → Skip, research is the answer
- User explicitly said "just investigate" → Skip, open-ended research

**Output Format**:
```
I have a few quick questions before I start researching:

1. [First question with multiple choice options]

[Wait for response, then ask next question if needed]
```

Only proceed to Step 1.5 (Load Coding Standards) after getting answers or determining questions aren't needed.

### Step 1.5: Load Coding Standards (If Present)

Before decomposing the research query, check for repository coding standards:

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
     1. Key architectural patterns (e.g., package structure, file organization)
     2. Critical anti-patterns to avoid
     3. Technology-specific guidelines (e.g., async usage, dependency management)
     4. Code quality standards (formatting, testing, imports)

     Format as a concise summary with specific file:line references for each guideline.
     Limit response to essential patterns only - focus on what would impact development decisions.
     ```

   - Wait for the sub-agent to complete before proceeding
   - Store the synthesized standards in context for reference during analysis

3. **If no standards found**:
   - Continue normally without standards (graceful degradation)
   - No need to mention absence to the user

**IMPORTANT**: Standards loading should happen BEFORE decomposing the research query, so architectural patterns can inform which components to investigate.

### Step 2: Analyze and Decompose
- Break down the user's query into composable research areas
- Take time to think deeply about the underlying patterns, connections, and architectural implications
- Identify specific components, patterns, or concepts to investigate
- Create a research plan using TodoWrite to track all subtasks
- Consider which directories, files, or architectural patterns are relevant

### Step 3: Spawn Parallel Sub-Agent Tasks
Create multiple Task agents to research different aspects concurrently:

**For codebase research:**
- Use the **codebase-locator** agent to find WHERE files and components live
- Use the **codebase-analyzer** agent to understand HOW specific code works
- Use the **codebase-pattern-finder** agent if you need examples of similar implementations

**For web research (only if user explicitly asks):**
- Use the **web-search-researcher** agent for external documentation and resources
- IF you use web-research agents, instruct them to return LINKS with their findings

The key is to use these agents intelligently:
- Start with locator agents to find what exists
- Then use analyzer agents on the most promising findings
- Run multiple agents in parallel when they're searching for different things
- Each agent knows its job - just tell it what you're looking for
- Don't write detailed prompts about HOW to search - the agents already know

### Step 4: Wait and Synthesize
- **IMPORTANT**: Wait for ALL sub-agent tasks to complete before proceeding
- Compile all sub-agent results
- Connect findings across different components
- **If coding standards were loaded**: Cross-reference findings with established patterns
  - Note where current implementation follows standards
  - Highlight any deviations from documented patterns
  - Reference specific standards when applicable (e.g., "Uses async pattern contrary to docs/coding-standards/repo-standards.md:240")
- Include specific file paths and line numbers for reference
- Highlight patterns, connections, and architectural decisions
- Answer the user's specific questions with concrete evidence

### Step 5: Generate Research Document

**IMPORTANT**: After generating the research document, complete the "Research Validation Checks" section at the end to ensure no hallucinations or placeholders remain.

### Username Detection for File Naming

Before creating the research document, detect the username to use in the filename:

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
   - Example: `2025.11.13-benjamin-authentication-flow.md`
   - Example: `2025.11.13-shared-api-documentation.md`

Create the document at `thoughts/research/YYYY.MM.DD-{username}-description.md` with this structure:

```markdown
---
date: [Current ISO datetime with timezone]
researcher: [Your name]
git_commit: [Current commit hash if available]
branch: [Current branch name if available]
repository: [Repository name]
topic: "[User's Question/Topic]"
tags: [research, codebase, relevant-component-names]
status: complete
last_updated: [Current date in YYYY-MM-DD format]
last_updated_by: [Your name]
---

# Research: [User's Question/Topic]

**Date**: [Current ISO datetime]
**Researcher**: [Your name]
**Git Commit**: [If available]
**Branch**: [If available]
**Repository**: [Repository name]

## Research Question
[Original user query]

## Summary
[High-level findings answering the user's question - 2-3 paragraphs]

## Expected Repos Involved

**Primary Repository**: [repo name where main changes occur]

**Secondary Repositories**:
- [repo name]: [why it's involved - API consumer, shared model, etc.]
- [repo name]: [why it's involved]

**Rationale**: [Brief explanation of why these repos are involved based on research findings]

**Cross-Repo Dependencies**:
- [Repo A] → [Repo B]: [nature of dependency - API call, shared model, etc.]

## Detailed Findings

### [Component/Area 1]
- Finding with reference ([file.ext:line](link))
- Connection to other components
- Implementation details

### [Component/Area 2]
...

## Code References
- `path/to/file.py:123` - Description of what's there
- `another/file.ts:45-67` - Description of the code block

## Architecture Insights
[Patterns, conventions, and design decisions discovered]

## Integration Points

[**Only include this section if the feature spans multiple repos or services**]

### API Calls Between Services:
- **[Service A] → [Service B]**:
  - Endpoint: `[HTTP method] /path/to/endpoint`
  - Purpose: [what data is exchanged]
  - File reference: `service-a/file.py:123`
  - OpenAPI client used: [yes/no, which client]

### Shared Data Models/Schemas:
- **[Model Name]**:
  - Defined in: `repo/path/to/model.py:45`
  - Used by: [list repos/services]
  - Schema validation: [where defined]

### Database Changes Required:
- **[Table name]**:
  - Changes: [new columns, indices, etc.]
  - Migration location: [path to migration]
  - Affects repos: [list]

### External Dependencies:
- **[Library/Service name]**:
  - Purpose: [why needed]
  - Integration pattern: [how it's used]
  - Configuration: [where config lives]

## Coding Standards Adherence
[**Only include this section if coding standards were loaded**]

**Standards Location**: `docs/coding-standards/*.md`

### Patterns Followed:
- [Pattern from standards that current code follows] - Reference: repo-standards.md:123
- [Another pattern that's being used correctly]

### Deviations Found:
- [Deviation from documented standards] - Reference: repo-standards.md:240
  - Current implementation: [what exists]
  - Expected per standards: [what standards recommend]
  - Impact: [Low/Medium/High]

### Recommendations:
- [Suggestion for aligning with standards, if relevant to research query]

## Related Research
[Links to other research documents if available]

## Questions for Hardened Requirements

**These questions MUST be answered before implementation begins. If research couldn't answer them, flag them explicitly.**

### Integration Questions:
- [ ] Have all API contracts between services been identified?
- [ ] Are OpenAPI client versions compatible across repos?
- [ ] Are shared data model schemas aligned?
- [ ] Have database migration dependencies been mapped?

### Data Flow Questions:
- [ ] How does data move between [Component A] and [Component B]?
- [ ] What happens if [Service X] is unavailable?
- [ ] Are there race conditions in the data flow?
- [ ] What validation happens at each boundary?

### Edge Case Questions:
- [ ] What happens when [expected condition] fails?
- [ ] How are errors propagated across service boundaries?
- [ ] What are the rollback procedures if deployment fails?
- [ ] Are there backwards compatibility concerns?

### Testing Questions:
- [ ] Can this be tested in isolation or does it require full integration?
- [ ] What test data is needed?
- [ ] Are there existing test patterns to follow?
- [ ] What's the acceptance test that proves this works?

**Unanswered Questions**:
[List any questions above that research could not answer and require CTO input or further investigation]

## Research Validation Checks

**Before finalizing this research document, verify:**

- [ ] **File Verification**: All mentioned file paths have been confirmed to exist using Read tool
- [ ] **Code Reference Verification**: All `file:line` references have been verified against actual code
- [ ] **Test Execution**: If claiming functionality works, tests were run and output verified
- [ ] **No Placeholders**: No sections contain placeholder text like "[TODO]" or "[TBD]"

**If any checks fail, update the research document before marking as complete.**

## Next Steps
[Recommended actions based on the research]
```

### Step 6: Present Findings
- Present a concise summary of findings to the user
- Include key file references for easy navigation
- Provide mermaid charts, when relevant, to facilitate understanding
- Ask if they have follow-up questions or need clarification

### Step 7: Handle Follow-ups
- If the user has follow-up questions, append to the same research document
- Update the frontmatter fields `last_updated` and `last_updated_by`
- Add a new section: `## Follow-up Research [timestamp]`
- Spawn new sub-agents as needed for additional investigation

## Important Notes

- Always use parallel Task agents to maximize efficiency and minimize context usage
- Focus on finding concrete file paths and line numbers for developer reference
- Research documents should be self-contained with all necessary context
- Each sub-agent prompt should be specific and focused on read-only operations
- Consider cross-component connections and architectural patterns
- Include temporal context (when the research was conducted)
- Keep the main agent focused on synthesis, not deep file reading
- Encourage sub-agents to find examples and usage patterns, not just definitions
- **File reading**: Always read mentioned files FULLY (no limit/offset) before spawning sub-tasks
- **Critical ordering**: Follow the numbered steps exactly
- **NEVER** write the research document with placeholder values

## Success Indicators

Good research documents:
- Answer the user's question completely
- Provide concrete code references
- Provide mermaid charts, when relevant, to facilitate understanding
- Identify patterns and connections
- Are immediately actionable
- Include enough context for future reference
