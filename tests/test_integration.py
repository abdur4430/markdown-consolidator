"""Integration tests for the full markdown consolidator pipeline."""

import sys
from pathlib import Path


def test_full_pipeline_analyze_then_synthesize(tmp_path, monkeypatch):
    """
    Given: A directory with related markdown files
    When: Running analyze then synthesize
    Then: Creates consolidated output files
    """
    from markdown_consolidator.cli import analyze_sections_cmd, synthesize_manifest_cmd

    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()

    # Create related files with enough content for chunking
    (source / "oauth-setup.md").write_text("""# OAuth Guide
## OAuth Configuration
Configure OAuth client credentials and redirect URIs for your application.
This involves setting up the authorization server and registering your app.

## Token Refresh
How to refresh expired OAuth tokens using the refresh token flow.
The refresh token allows obtaining new access tokens without user interaction.
""")

    (source / "auth-flow.md").write_text("""# Authentication
## Login Flow
User authentication login process with session management and security features.
This includes handling credentials, validating users, and creating sessions.

## Logout Flow
Proper session termination and cleanup when users sign out of the application.
Clear all tokens, cookies, and cached authentication state properly.
""")

    (source / "database.md").write_text("""# Database
## Schema Design
PostgreSQL table design and relationships for the application data model.
Includes primary keys, foreign keys, indexes, and constraints for performance.
""")

    manifest_path = tmp_path / "manifest.yaml"

    # Step 1: Analyze
    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(manifest_path)]
    )
    result = analyze_sections_cmd()
    assert result == 0
    assert manifest_path.exists()

    # Check manifest has expected content
    manifest_content = manifest_path.read_text()
    assert 'hierarchy' in manifest_content
    assert 'source' in manifest_content

    # Step 2: Synthesize
    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-synthesize-manifest', str(manifest_path), str(output)]
    )
    result = synthesize_manifest_cmd()
    assert result == 0

    # Should have created files
    output_files = list(output.glob('*.md'))
    assert len(output_files) >= 1


def test_pipeline_with_duplicates(tmp_path, monkeypatch):
    """
    Given: Files with duplicate sections (same fingerprint)
    When: Running the pipeline
    Then: Duplicates are detected and marked in manifest
    """
    from markdown_consolidator.cli import analyze_sections_cmd

    source = tmp_path / "source"
    source.mkdir()

    # Create files with identical content
    identical_content = """# Doc
## OAuth Setup
Configure OAuth client credentials and redirect URIs for your application.
This involves setting up the authorization server and registering your app.
"""
    (source / "doc1.md").write_text(identical_content)
    (source / "doc2.md").write_text(identical_content)

    manifest_path = tmp_path / "manifest.yaml"

    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(manifest_path)]
    )
    result = analyze_sections_cmd()
    assert result == 0

    # Manifest should show duplicates
    manifest_content = manifest_path.read_text()
    # Either mentions duplicates_removed or has duplicate_of in the output
    assert 'duplicates_removed' in manifest_content or 'duplicate_of' in manifest_content


def test_pipeline_preserves_content(tmp_path, monkeypatch):
    """
    Given: A source file with specific content
    When: Running analyze then synthesize
    Then: Output preserves the essential content
    """
    from markdown_consolidator.cli import analyze_sections_cmd, synthesize_manifest_cmd

    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()

    unique_phrase = "UNIQUE_TEST_PHRASE_12345"
    (source / "test.md").write_text(f"""# Test Doc
## Important Section
This section contains a {unique_phrase} that must be preserved.
Additional content here to meet the minimum word count requirement.
""")

    manifest_path = tmp_path / "manifest.yaml"

    # Analyze
    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(manifest_path)]
    )
    analyze_sections_cmd()

    # Synthesize
    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-synthesize-manifest', str(manifest_path), str(output)]
    )
    synthesize_manifest_cmd()

    # Check content is preserved
    output_files = list(output.glob('*.md'))
    assert len(output_files) >= 1
    content = output_files[0].read_text()
    assert unique_phrase in content


def test_empty_directory_handling(tmp_path, monkeypatch, capsys):
    """
    Given: An empty directory
    When: Running analyze
    Then: Exits gracefully with appropriate message
    """
    from markdown_consolidator.cli import analyze_sections_cmd

    source = tmp_path / "source"
    source.mkdir()

    manifest_path = tmp_path / "manifest.yaml"

    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(manifest_path)]
    )
    result = analyze_sections_cmd()
    assert result == 0

    captured = capsys.readouterr()
    assert "No sections found" in captured.out


def test_chunker_embedder_keywords_integration():
    """
    Given: Raw markdown content
    When: Processing through chunker, embedder, and keywords
    Then: Sections have all required fields
    """
    import tempfile
    from markdown_consolidator.chunker import MarkdownChunker
    from markdown_consolidator.embedder import Embedder
    from markdown_consolidator.keywords import KeywordExtractor

    with tempfile.TemporaryDirectory() as tmpdir:
        md_file = Path(tmpdir) / "test.md"
        md_file.write_text("""# Test
## OAuth Authentication
Configure OAuth client credentials and redirect URIs for secure authentication.
This involves setting up the authorization server and registering your application.

## Database Schema
Design PostgreSQL tables with proper relationships and constraints for data integrity.
Includes primary keys, foreign keys, indexes, and proper normalization strategies.
""")

        # Chunk
        chunker = MarkdownChunker()
        sections = chunker.chunk_file(md_file)
        assert len(sections) == 2

        # Embed
        embedder = Embedder()
        sections = embedder.embed_sections(sections)
        for s in sections:
            assert 'embedding' in s
            assert len(s['embedding']) == 384

        # Keywords
        extractor = KeywordExtractor()
        sections = extractor.extract_keywords(sections)
        for s in sections:
            assert 'keywords' in s
            assert len(s['keywords']) > 0


def test_tree_builder_manifest_integration():
    """
    Given: Sections with embeddings
    When: Building hierarchy and generating manifest
    Then: Manifest has valid structure
    """
    import yaml
    from markdown_consolidator.tree_builder import TreeBuilder
    from markdown_consolidator.manifest import ManifestGenerator

    sections = [
        {
            'section_id': 'test.md/OAuth',
            'heading': 'OAuth',
            'content': 'OAuth content',
            'embedding': [1.0] * 384,
            'keywords': ['oauth', 'auth'],
            'fingerprint': 'abc123',
            'last_modified': '2025-12-08',
            'source_file': '/path/test.md',
        },
        {
            'section_id': 'test.md/Login',
            'heading': 'Login',
            'content': 'Login content',
            'embedding': [0.9, 0.1] + [0.0] * 382,
            'keywords': ['login', 'auth'],
            'fingerprint': 'def456',
            'last_modified': '2025-12-08',
            'source_file': '/path/test.md',
        },
    ]

    builder = TreeBuilder(threshold=0.5)
    hierarchy = builder.build_hierarchy(sections)

    assert 'themes' in hierarchy
    assert 'orphans' in hierarchy

    generator = ManifestGenerator(source_dir='./docs', threshold=0.5)
    manifest_str = generator.generate(hierarchy, total_sections=2, duplicates_removed=0)

    # Should be valid YAML
    parsed = yaml.safe_load(manifest_str)
    assert 'hierarchy' in parsed
    assert parsed['total_sections'] == 2
