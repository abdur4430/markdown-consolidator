"""
Tests for encapsulation scoring module.
"""

import pytest


def test_encapsulation_scorer_high_coherence():
    """
    Given: A header that accurately describes its content
    When: Computing encapsulation score
    Then: Score should be > 0.7
    """
    from markdown_consolidator.encapsulation import EncapsulationScorer

    scorer = EncapsulationScorer()

    score = scorer.score_encapsulation(
        header="User Authentication Flow",
        content="This section describes how users authenticate using OAuth2. "
                "The flow involves redirecting to the identity provider, "
                "receiving an authorization code, and exchanging it for tokens.",
    )

    assert score > 0.7


def test_encapsulation_scorer_low_coherence():
    """
    Given: A generic header that doesn't describe specific content
    When: Computing encapsulation score
    Then: Score should be < 0.5
    """
    from markdown_consolidator.encapsulation import EncapsulationScorer

    scorer = EncapsulationScorer()

    score = scorer.score_encapsulation(
        header="Notes",
        content="The database migration requires PostgreSQL 14 or higher. "
                "Make sure to backup all data before running the migration script. "
                "The estimated downtime is 30 minutes for large datasets.",
    )

    assert score < 0.5


def test_encapsulate_sections_adds_scores():
    """
    Given: A list of sections with heading and content
    When: Running encapsulate_sections
    Then: Each section has encapsulation_score key added
    """
    from markdown_consolidator.encapsulation import EncapsulationScorer

    sections = [
        {
            'section_id': 'doc1/OAuth Setup',
            'heading': 'OAuth Setup',
            'content': 'Configure OAuth by registering your application...',
        },
        {
            'section_id': 'doc1/Notes',
            'heading': 'Notes',
            'content': 'Database requires PostgreSQL 14. Also check memory limits.',
        },
    ]

    scorer = EncapsulationScorer()
    result = scorer.encapsulate_sections(sections)

    assert len(result) == 2
    assert 'encapsulation_score' in result[0]
    assert 'encapsulation_score' in result[1]
    assert isinstance(result[0]['encapsulation_score'], float)
    assert 0.0 <= result[0]['encapsulation_score'] <= 1.0
    # Verify OAuth section scores higher than generic "Notes"
    assert result[0]['encapsulation_score'] > result[1]['encapsulation_score']


def test_encapsulate_sections_empty_input():
    """
    Given: An empty list of sections
    When: Running encapsulate_sections
    Then: Returns empty list without error
    """
    from markdown_consolidator.encapsulation import EncapsulationScorer

    scorer = EncapsulationScorer()
    result = scorer.encapsulate_sections([])

    assert result == []
