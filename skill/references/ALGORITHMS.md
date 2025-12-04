# Consolidation Algorithms Reference

## Similarity Detection

### TF-IDF Cosine Similarity

The primary algorithm for detecting content similarity between markdown files.

**Process:**
1. Tokenize each document (lowercase, remove punctuation, filter stopwords)
2. Compute term frequency (TF) for each term in each document
3. Compute inverse document frequency (IDF) across all documents
4. Create TF-IDF weighted vectors
5. Compute cosine similarity between document pairs

**Formula:**
```
TF(t,d) = count(t in d) / max_count(d)
IDF(t) = log(N / df(t))
TF-IDF(t,d) = TF(t,d) × IDF(t)

cosine_sim(d1, d2) = (v1 · v2) / (||v1|| × ||v2||)
```

**Threshold Guidelines:**
- `0.8+`: Near-duplicate content (likely copy-paste with minor edits)
- `0.6-0.8`: Strongly related content (same topic, significant overlap)
- `0.4-0.6`: Moderately related (similar domain, some shared concepts)
- `0.2-0.4`: Weakly related (tangential connection)
- `<0.2`: Unrelated

### Content Fingerprinting

Fast duplicate detection using MD5 hashes of normalized content.

**Normalization steps:**
1. Convert to lowercase
2. Remove all punctuation
3. Collapse whitespace
4. Hash the result

**Use cases:**
- Exact section duplicate detection
- Quick deduplication passes
- Identifying copy-paste content

## Clustering Methods

### Topic Clustering

Groups files by content similarity using connected components.

**Algorithm:**
1. Build similarity graph (nodes = files, edges = similarity > threshold)
2. Find connected components using depth-first search
3. Each component becomes a cluster
4. Calculate cluster cohesion as average internal similarity

**Pros:** Natural grouping, handles variable cluster sizes
**Cons:** Sensitive to threshold, can create very large clusters

### Temporal Clustering

Groups files modified within a time window.

**Algorithm:**
1. Sort files by modification time
2. Slide window of specified duration
3. Group files within each window
4. Merge overlapping windows

**Use cases:**
- Project sprint consolidation
- Session-based work grouping
- Evolution tracking

### Hierarchical Clustering

Combines directory structure with content similarity.

**Algorithm:**
1. Group files by parent directory
2. Calculate within-directory similarity
3. Split low-cohesion directories
4. Merge high-similarity cross-directory files

**Use cases:**
- Organized codebases
- Documentation with clear structure
- Mixed-content repositories

### Link-Based Clustering

Groups files based on internal reference patterns.

**Algorithm:**
1. Parse wikilinks and markdown links
2. Build directed graph
3. Find strongly connected components
4. Include referenced but non-linking files

## Conflict Detection

### Numeric Conflict Detection

Identifies files with different numbers in similar contexts.

**Process:**
1. Extract all numeric patterns from each file
2. Compare numeric sets between similar files
3. Flag differences as potential conflicts

**Patterns detected:**
- Integers: `\b\d+\b`
- Decimals: `\b\d+\.\d+\b`
- Dates: Various formats
- Versions: `v?\d+\.\d+(\.\d+)?`

### Semantic Conflict Detection

Identifies contradictory statements (requires LLM integration).

**Approach:**
1. Extract key assertions from each file
2. Compare assertions for logical consistency
3. Flag contradictions for review

## Merge Strategies

### Authority-Based Merge

Most recent file takes precedence for conflicts.

```python
def resolve_conflict(versions):
    return max(versions, key=lambda v: v.modified_date)
```

**When to use:**
- Documentation that evolves over time
- Knowledge that gets refined
- Single-author workflows

### Comprehensive Merge

Preserves all unique information.

```python
def merge_sections(sections):
    unique = deduplicate(sections)
    conflicts = find_conflicts(sections)
    return {
        'content': combine(unique),
        'conflicts': conflicts  # For manual review
    }
```

**When to use:**
- Knowledge bases needing completeness
- Multi-author content
- Research notes

### Canonical Merge

Single source of truth with references.

```python
def create_canonical(primary, supporting):
    return {
        'main_content': primary.content,
        'references': [s.metadata for s in supporting],
        'history': build_history(primary, supporting)
    }
```

**When to use:**
- Specifications
- Official documentation
- Versioned content
