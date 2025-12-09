"""
Generate summaries for sections using Ollama.
"""

from __future__ import annotations

from typing import Any

import httpx


class Summarizer:
    """Generate summaries using local Ollama LLM."""

    def __init__(
        self,
        model: str = "llama3.2:3b",
        base_url: str = "http://localhost:11434",
        timeout: float = 30.0,
    ):
        """
        Initialize summarizer.

        Parameters
        ----------
        model : str
            Ollama model name.
        base_url : str
            Ollama API base URL.
        timeout : float
            Request timeout in seconds.
        """
        self.model = model
        self.base_url = base_url
        self.timeout = timeout

    def _generate(self, prompt: str) -> str | None:
        """Generate text from Ollama."""
        try:
            response = httpx.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json().get('response', '').strip()
        except Exception:
            return None

    def summarize_sections(self, sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """
        Add summaries to sections.

        Parameters
        ----------
        sections : list[dict]
            List of section dicts with 'content' and 'heading' keys.

        Returns
        -------
        list[dict]
            Same sections with 'summary' key added.
        """
        if not sections:
            return sections

        for section in sections:
            heading = section.get('heading', '')
            content = section.get('content', '')[:1000]  # Limit context

            prompt = f"""Summarize this documentation section in one sentence (max 100 characters).

Section: {heading}

Content:
{content}

Summary:"""

            summary = self._generate(prompt)
            section['summary'] = summary

        return sections
