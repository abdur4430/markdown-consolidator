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
