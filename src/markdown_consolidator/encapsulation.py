"""
Score header-content encapsulation using semantic similarity.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import numpy as np
from sentence_transformers import SentenceTransformer


class EncapsulationScorer:
    """Score how well headers describe their content."""

    def __init__(
        self,
        *,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        threshold: float = 0.5,
    ):
        """
        Initialize encapsulation scorer.

        Parameters
        ----------
        model_name : str
            HuggingFace model name for sentence-transformers.
        threshold : float
            Score below which a section is considered poorly encapsulated.
        """
        self.model = SentenceTransformer(model_name)
        self.threshold = threshold

    def score_encapsulation(self, *, header: str, content: str) -> float:
        """
        Compute encapsulation score between header and content.

        Parameters
        ----------
        header : str
            The section header text.
        content : str
            The section content text.

        Returns
        -------
        float
            Score between 0.0 and 1.0, higher means better encapsulation.
        """
        if not header or not content:
            return 0.0

        # Truncate content to model's context window
        content_truncated = content[:2000]

        # Encode both as vectors
        embeddings = self.model.encode(
            [header, content_truncated],
            convert_to_numpy=True,
        )

        header_emb = embeddings[0]
        content_emb = embeddings[1]

        # Cosine similarity
        dot_product = np.dot(header_emb, content_emb)
        norms = np.linalg.norm(header_emb) * np.linalg.norm(content_emb)

        if norms < 1e-10:
            return 0.0

        return float(dot_product / norms)

    def encapsulate_sections(
        self,
        sections: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Add encapsulation scores to all sections.

        Parameters
        ----------
        sections : list[dict[str, Any]]
            List of section dicts with 'heading' and 'content' keys.

        Returns
        -------
        list[dict[str, Any]]
            Same sections with 'encapsulation_score' key added.
        """
        if not sections:
            return sections

        for section in sections:
            section['encapsulation_score'] = self.score_encapsulation(
                header=section.get('heading', ''),
                content=section.get('content', ''),
            )

        return sections


class Rechunker:
    """Split poorly-encapsulated sections using LLM."""

    def __init__(
        self,
        *,
        model: str = "llama3.2:3b",
        base_url: str = "http://localhost:11434",
        timeout: float = 60.0,
        threshold: float = 0.5,
    ):
        """
        Initialize rechunker.

        Parameters
        ----------
        model : str
            Ollama model name.
        base_url : str
            Ollama API base URL.
        timeout : float
            Request timeout in seconds.
        threshold : float
            Encapsulation score below which to rechunk.
        """
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self.threshold = threshold

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

    def rechunk_section(
        self,
        section: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Split a poorly-encapsulated section into multiple sections.

        Parameters
        ----------
        section : dict[str, Any]
            Section dict with encapsulation_score.

        Returns
        -------
        list[dict[str, Any]]
            List of new sections (or original if well-encapsulated).
        """
        score = section.get('encapsulation_score', 1.0)
        if score >= self.threshold:
            return [section]

        content = section.get('content', '')[:3000]
        heading = section.get('heading', '')

        prompt = f"""Analyze this documentation section and split it into logical sub-sections.

Current Header: {heading}

Content:
{content}

This section mixes multiple topics. Split it into 2-4 focused sections.

Return ONLY a JSON array with objects containing "header" and "content" keys:
[{{"header": "New Header 1", "content": "Content for section 1..."}}, ...]

JSON:"""

        response = self._generate(prompt)
        if not response:
            return [section]

        try:
            # Parse JSON from response
            parsed = json.loads(response)
            if not isinstance(parsed, list) or len(parsed) < 2:
                return [section]

            # Create new sections
            new_sections = []
            for i, item in enumerate(parsed):
                new_sections.append({
                    'section_id': f"{section['section_id']}/{i+1}",
                    'heading': item.get('header', f"Part {i+1}"),
                    'content': item.get('content', ''),
                    'source_file': section.get('source_file', ''),
                    'rechunked_from': section['section_id'],
                })

            return new_sections

        except (json.JSONDecodeError, KeyError, TypeError):
            return [section]

    def rechunk_sections(
        self,
        sections: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Rechunk all poorly-encapsulated sections.

        Parameters
        ----------
        sections : list[dict[str, Any]]
            Sections with encapsulation_score.

        Returns
        -------
        list[dict[str, Any]]
            Sections with poor ones split into multiple.
        """
        result = []
        for section in sections:
            result.extend(self.rechunk_section(section))
        return result
