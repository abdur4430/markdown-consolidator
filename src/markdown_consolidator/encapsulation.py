"""
Score header-content encapsulation using semantic similarity.
"""

from __future__ import annotations

from typing import Any

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
