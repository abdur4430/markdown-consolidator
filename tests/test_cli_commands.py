"""Tests for the new CLI commands."""

import sys


def test_cli_analyze_creates_manifest(tmp_path, monkeypatch):
    """
    Given: A directory with markdown files
    When: Running 'mdconsolidate-analyze' (new H2 section analyzer)
    Then: Creates a manifest.yaml file
    """
    from markdown_consolidator.cli import analyze_sections_cmd

    source = tmp_path / "source"
    source.mkdir()
    # Need at least 10 words per section for chunker min_section_words default
    (source / "test.md").write_text("""# Test
## Section One
This is content with enough words to pass the minimum word count requirement.
The chunker needs at least ten words to consider this a valid section.
""")

    output_manifest = tmp_path / "manifest.yaml"

    # Simulate command line args
    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(output_manifest)]
    )

    result = analyze_sections_cmd()

    assert result == 0
    assert output_manifest.exists()

    # Check manifest content
    content = output_manifest.read_text()
    assert 'hierarchy' in content
    assert 'source' in content


def test_cli_synthesize_from_manifest_creates_files(tmp_path, monkeypatch):
    """
    Given: A manifest file
    When: Running 'mdconsolidate-synthesize-manifest'
    Then: Creates output markdown files
    """
    from markdown_consolidator.cli import synthesize_manifest_cmd

    source = tmp_path / "source"
    output = tmp_path / "output"
    source.mkdir()
    (source / "test.md").write_text("# Test\n## OAuth\nOAuth content here with enough words.")

    manifest_content = f"""source: {source}
hierarchy:
  - theme: Auth
    confidence: 0.9
    documents:
      - name: auth.md
        sections:
          - id: test.md/OAuth
            heading: OAuth
orphans: []
"""
    manifest_file = tmp_path / "manifest.yaml"
    manifest_file.write_text(manifest_content)

    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-synthesize-manifest', str(manifest_file), str(output)]
    )

    result = synthesize_manifest_cmd()

    assert result == 0
    assert (output / 'auth.md').exists()


def test_cli_analyze_with_no_sections(tmp_path, monkeypatch, capsys):
    """
    Given: A directory with markdown files without H2 sections
    When: Running analyze
    Then: Exits gracefully with message
    """
    from markdown_consolidator.cli import analyze_sections_cmd

    source = tmp_path / "source"
    source.mkdir()
    (source / "test.md").write_text("# Just a title\n\nNo H2 sections here.")

    output_manifest = tmp_path / "manifest.yaml"

    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(output_manifest)]
    )

    result = analyze_sections_cmd()

    assert result == 0
    captured = capsys.readouterr()
    assert "No sections found" in captured.out


def test_cli_analyze_with_threshold_option(tmp_path, monkeypatch):
    """
    Given: A directory with markdown files
    When: Running analyze with custom threshold
    Then: Uses the specified threshold
    """
    from markdown_consolidator.cli import analyze_sections_cmd

    source = tmp_path / "source"
    source.mkdir()
    # Need at least 10 words per section for chunker min_section_words default
    (source / "test.md").write_text("""# Test
## Section
This is content with enough words to pass the minimum word count requirement.
The chunker needs at least ten words to consider this a valid section.
""")

    output_manifest = tmp_path / "manifest.yaml"

    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--output', str(output_manifest), '--threshold', '0.7']
    )

    result = analyze_sections_cmd()

    assert result == 0
    content = output_manifest.read_text()
    assert 'threshold: 0.7' in content


def test_analyze_sections_with_encapsulation(tmp_path, monkeypatch):
    """
    Given: A directory with markdown files
    When: Running analyze-sections with --encapsulate flag
    Then: Manifest contains encapsulation_score for each section
    """
    import yaml

    from markdown_consolidator.cli import analyze_sections_cmd

    # Setup test files
    source = tmp_path / "source"
    source.mkdir()
    (source / "test.md").write_text(
        "# Document\n\n"
        "## OAuth Authentication\n\n"
        "This explains OAuth authentication flow with enough words "
        "to pass the minimum word count requirement for chunking.\n\n"
        "## Notes\n\n"
        "Random notes about various topics including databases "
        "and memory limits that are not related to the header.\n"
    )
    output_manifest = tmp_path / "manifest.yaml"

    monkeypatch.setattr(
        sys, 'argv',
        ['mdconsolidate-analyze-sections', str(source), '--encapsulate',
         '--output', str(output_manifest)]
    )

    result = analyze_sections_cmd()

    assert result == 0
    assert output_manifest.exists()

    manifest = yaml.safe_load(output_manifest.read_text())
    # Find sections in hierarchy
    themes = manifest['hierarchy']
    assert len(themes) > 0
    sections = themes[0]['documents'][0]['sections']
    assert 'encapsulation_score' in sections[0]
