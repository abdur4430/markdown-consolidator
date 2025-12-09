"""Tests for the summarizer module."""
import pytest


def test_summarizer_generates_summaries(mocker):
    """
    Given: Sections with content
    When: Summarizing with Ollama
    Then: Each section gets a summary
    """
    from markdown_consolidator.summarizer import Summarizer

    # Mock httpx to avoid actual Ollama calls in tests
    mock_response = mocker.Mock()
    mock_response.json.return_value = {'response': 'This section explains OAuth setup.'}
    mock_response.raise_for_status = mocker.Mock()

    mocker.patch('httpx.post', return_value=mock_response)

    sections = [
        {'section_id': 'a', 'heading': 'OAuth', 'content': 'OAuth requires client credentials...'},
    ]

    summarizer = Summarizer(model="llama3.2:3b")
    result = summarizer.summarize_sections(sections)

    assert result[0]['summary'] == 'This section explains OAuth setup.'


def test_summarizer_handles_ollama_unavailable(mocker):
    """
    Given: Ollama is not running
    When: Attempting to summarize
    Then: Sections get summary=None without crashing
    """
    import httpx

    from markdown_consolidator.summarizer import Summarizer

    mocker.patch('httpx.post', side_effect=httpx.ConnectError("Connection refused"))

    sections = [{'section_id': 'a', 'heading': 'Test', 'content': 'Some content'}]

    summarizer = Summarizer()
    result = summarizer.summarize_sections(sections)

    assert result[0]['summary'] is None


def test_summarizer_handles_empty_input():
    """
    Given: Empty list of sections
    When: Summarizing
    Then: Returns empty list without error
    """
    from markdown_consolidator.summarizer import Summarizer

    summarizer = Summarizer()
    result = summarizer.summarize_sections([])

    assert result == []
