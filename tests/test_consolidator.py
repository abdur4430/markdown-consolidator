"""
Tests for markdown-consolidator.
"""

import tempfile
from pathlib import Path

import pytest


def test_version():
    """Test that version is accessible."""
    from markdown_consolidator import __version__
    assert __version__ == "0.1.0"


def test_inventory_empty_directory():
    """Test inventory on empty directory."""
    from markdown_consolidator import inventory_directory
    
    with tempfile.TemporaryDirectory() as tmpdir:
        result = inventory_directory(directory=Path(tmpdir))
        assert result == []


def test_inventory_single_file():
    """Test inventory with a single markdown file."""
    from markdown_consolidator import inventory_directory
    
    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = Path(tmpdir) / "test.md"
        md_file.write_text("# Test\n\nHello world")

        result = inventory_directory(directory=Path(tmpdir))
        
        assert len(result) == 1
        assert result[0]['filename'] == 'test.md'
        assert result[0]['title'] == 'Test'
        assert result[0]['word_count'] >= 2  # "Hello world" at minimum


def test_extract_frontmatter():
    """Test frontmatter extraction."""
    from markdown_consolidator.inventory import extract_frontmatter
    
    content = """---
title: Test Document
tags: [a, b]
---

# Content here
"""
    frontmatter, body = extract_frontmatter(content=content)
    
    assert frontmatter['title'] == 'Test Document'
    assert frontmatter['tags'] == ['a', 'b']
    assert '# Content here' in body


def test_extract_links():
    """Test link extraction."""
    from markdown_consolidator.inventory import extract_links
    
    content = """
Check [[wikilink]] and [[another|display]].
Also [markdown](link.md) and [external](https://example.com).
"""
    links = extract_links(content=content)
    
    assert 'wikilink' in links['internal']
    assert 'another' in links['internal']
    assert 'link.md' in links['internal']
    assert len(links['external']) == 1
    assert links['external'][0]['url'] == 'https://example.com'


def test_compute_fingerprint():
    """Test content fingerprinting."""
    from markdown_consolidator.inventory import compute_fingerprint
    
    fp1 = compute_fingerprint(content="Hello World!")
    fp2 = compute_fingerprint(content="hello world")
    fp3 = compute_fingerprint(content="Something else")
    
    # Same content (normalized) should have same fingerprint
    assert fp1 == fp2
    # Different content should have different fingerprint
    assert fp1 != fp3


def test_cosine_similarity():
    """Test cosine similarity calculation."""
    from markdown_consolidator.relationships import cosine_similarity
    
    vec1 = {'a': 1.0, 'b': 2.0}
    vec2 = {'a': 1.0, 'b': 2.0}
    vec3 = {'c': 1.0, 'd': 2.0}
    
    # Identical vectors
    assert cosine_similarity(vec1=vec1, vec2=vec2) == pytest.approx(1.0)
    # No overlap
    assert cosine_similarity(vec1=vec1, vec2=vec3) == 0.0


def test_topic_cluster():
    """Test topic clustering."""
    from markdown_consolidator.clustering import topic_cluster
    
    relationships = {
        'content_similarities': [
            {'file1': 'a.md', 'file2': 'b.md', 'similarity': 0.8},
            {'file1': 'b.md', 'file2': 'c.md', 'similarity': 0.7},
        ]
    }
    
    clusters = topic_cluster(relationships=relationships, threshold=0.6)
    
    assert len(clusters) == 1
    assert set(clusters[0]['files']) == {'a.md', 'b.md', 'c.md'}


def test_full_pipeline():
    """Test the full consolidation pipeline."""
    from markdown_consolidator import consolidate
    
    with tempfile.TemporaryDirectory() as tmpdir:
        source = Path(tmpdir) / "source"
        output = Path(tmpdir) / "output"
        source.mkdir()
        
        # Create test files with overlapping content
        (source / "file1.md").write_text("""---
title: File One
---
# Topic A

This is about topic A and some shared content.
""")
        (source / "file2.md").write_text("""---
title: File Two
---
# Topic A

This discusses topic A with shared content and more details.
""")
        
        result = consolidate(source_dir=source, output_dir=output, threshold=0.3)
        
        assert result['files_analyzed'] == 2
        assert result['output_directory'] == str(output)
        assert (output / '_consolidation_log.json').exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
