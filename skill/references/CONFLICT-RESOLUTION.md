# Conflict Resolution Patterns

## Conflict Types

### Type 1: Exact Duplicates

**Definition:** Identical content appearing in multiple files.

**Detection:** Content fingerprint matching.

**Resolution:** Keep first occurrence by modification date, remove duplicates.

```markdown
<!-- DEDUPLICATED: Removed duplicate from file-b.md -->
```

### Type 2: Near Duplicates

**Definition:** Content with minor variations (whitespace, punctuation, phrasing).

**Detection:** Similarity score > 0.9 with different fingerprints.

**Resolution Options:**
1. Keep most recent version
2. Keep longest version (most complete)
3. Flag for manual review

```markdown
<!-- NEAR-DUPLICATE: Merged from file-a.md (original) and file-b.md (variant) -->
```

### Type 3: Semantic Overlap

**Definition:** Same information expressed differently.

**Detection:** Similarity score 0.6-0.9 with shared key terms.

**Resolution:** Combine unique aspects, note sources.

```markdown
<!-- COMBINED: Synthesized from:
     - file-a.md: Original explanation
     - file-b.md: Added examples
     - file-c.md: Added edge cases
-->
```

### Type 4: Factual Conflicts

**Definition:** Contradictory information (numbers, dates, assertions).

**Detection:** Different values for same entity/metric.

**Resolution by Strategy:**

**Authority Strategy:**
```markdown
Token expiry: 24 hours
<!-- CONFLICT RESOLVED: Used file-a.md (2024-12-02) over file-b.md (2024-11-28) -->
```

**Comprehensive Strategy:**
```markdown
Token expiry:
- 24 hours (per file-a.md, 2024-12-02)
- 1 hour (per file-b.md, 2024-11-28)
<!-- TODO: Verify correct value -->
```

### Type 5: Structural Conflicts

**Definition:** Same section heading, different content.

**Detection:** Matching normalized heading, different section fingerprint.

**Resolution:** Merge section contents with clear attribution.

## Resolution Workflow

### Step 1: Categorize

```
For each conflict pair:
  if fingerprint match → Type 1 (exact)
  elif similarity > 0.9 → Type 2 (near)
  elif similarity > 0.6 → Type 3 (overlap)
  elif same_entities_different_values → Type 4 (factual)
  elif same_heading_different_content → Type 5 (structural)
```

### Step 2: Apply Strategy

```
For each conflict:
  if type in (1, 2) → auto_resolve(keep_newest)
  elif type == 3 → auto_merge(combine_unique)
  elif type == 4:
    if strategy == 'authority' → use_newest()
    else → flag_for_review()
  elif type == 5 → merge_sections()
```

### Step 3: Document

All resolutions include:
- Source files involved
- Resolution method applied
- Original values (for reversibility)
- Timestamp of resolution

## Conflict Markers

### In-Document Markers

```markdown
<!-- CONFLICT: topic="token_expiry" files="a.md,b.md" -->
**Unresolved:** Token expiry differs between sources.
- Source A (2024-12-02): 24 hours
- Source B (2024-11-28): 1 hour

**Action required:** Verify correct value with implementation.
<!-- END CONFLICT -->
```

### Resolution Markers

```markdown
<!-- RESOLVED: topic="token_expiry" 
     method="authority" 
     selected="a.md" 
     reason="most_recent" 
     resolved_at="2024-12-03T14:00:00" -->
```

### Review Request Markers

```markdown
<!-- REVIEW NEEDED -->
The following conflict requires manual resolution:

| Aspect | Source A | Source B |
|--------|----------|----------|
| Token expiry | 24 hours | 1 hour |
| Source | a.md | b.md |
| Modified | 2024-12-02 | 2024-11-28 |

- [ ] Verify correct value
- [ ] Update consolidated document
- [ ] Remove this marker
<!-- END REVIEW -->
```

## Best Practices

### 1. Preserve Reversibility

Always include enough information to undo a resolution:

```markdown
<!-- BACKUP: Original content from file-b.md
Token expiry is set to 1 hour for security reasons.
-->
```

### 2. Prefer Recency with Verification

Newest isn't always correct, but it's the best default:

```markdown
<!-- RESOLVED by recency, VERIFY if critical -->
```

### 3. Flag Uncertainty

When in doubt, don't auto-resolve:

```markdown
<!-- LOW CONFIDENCE RESOLUTION
     Similarity: 0.62 (borderline)
     Recommendation: Manual review
-->
```

### 4. Maintain Audit Trail

Log all resolutions for future reference:

```json
{
  "conflict_id": "c_001",
  "files": ["a.md", "b.md"],
  "type": "factual",
  "topic": "token_expiry",
  "values": {"a.md": "24h", "b.md": "1h"},
  "resolution": "a.md",
  "method": "authority",
  "resolved_at": "2024-12-03T14:00:00",
  "resolved_by": "auto"
}
```
