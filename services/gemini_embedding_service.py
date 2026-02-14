"""
Gemini Embedding Service

Integrates with Google Gemini API to generate embeddings for text chunks.
Based on official documentation: https://ai.google.dev/gemini-api/docs/embeddings

Model: gemini-embedding-001
Output dimensions: 768 (configurable, down from default 3,072)
Task types: RETRIEVAL_DOCUMENT for indexing, RETRIEVAL_QUERY for search
"""

import asyncio
from typing import Literal

import numpy as np
from google import genai
from google.genai import types


TaskType = Literal[
    "RETRIEVAL_DOCUMENT",
    "RETRIEVAL_QUERY",
    "SEMANTIC_SIMILARITY",
    "CLASSIFICATION",
    "CLUSTERING",
]


class GeminiEmbeddingService:
    """
    Service for generating text embeddings using Google Gemini API.

    Features:
    - Uses gemini-embedding-001 model
    - Configurable output dimensions (default 768)
    - Task-type optimization for retrieval
    - Automatic normalization for reduced dimensions
    - Batch processing support
    - Error handling and logging
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-embedding-001",
        output_dimensionality: int = 768,
        task_type: TaskType = "RETRIEVAL_DOCUMENT",
        batch_size: int = 100,
    ):
        """
        Initialize Gemini embedding service.

        Args:
            api_key: Google Gemini API key
            model: Embedding model to use (default: gemini-embedding-001)
            output_dimensionality: Output dimensions (128-3072, recommended: 768)
            task_type: Task type for optimization (RETRIEVAL_DOCUMENT for indexing)
            batch_size: Maximum texts per API call
        """
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.output_dimensionality = output_dimensionality
        self.task_type = task_type
        self.batch_size = batch_size

        # Normalization required for dimensions < 3072
        self.normalize = output_dimensionality < 3072

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts.

        Processes in batches and includes normalization for reduced dimensions.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (one per input text)

        Raises:
            ValueError: If texts list is empty
            Exception: On API errors
        """
        if not texts:
            raise ValueError("Cannot embed empty list of texts")

        all_embeddings = []

        # Process in batches
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i : i + self.batch_size]
            batch_embeddings = await self._embed_batch(batch)
            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    async def embed_single(self, text: str) -> list[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector

        Raises:
            Exception: On API errors
        """
        embeddings = await self.embed_texts([text])
        return embeddings[0]

    async def _embed_batch(self, texts: list[str]) -> list[list[float]]:
        """
        Call Gemini API to embed a batch of texts.

        Args:
            texts: Batch of texts to embed (max batch_size)

        Returns:
            List of embedding vectors (normalized if dimensions < 3072)

        Raises:
            Exception: On API errors
        """
        # Run sync Gemini API call in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(
                    task_type=self.task_type,
                    output_dimensionality=self.output_dimensionality,
                ),
            ),
        )

        # Extract embeddings from result
        embeddings = []
        for embedding_obj in result.embeddings:
            embedding_values = embedding_obj.values

            # Normalize if using reduced dimensions (< 3072)
            if self.normalize:
                embedding_np = np.array(embedding_values)
                normalized = embedding_np / np.linalg.norm(embedding_np)
                embeddings.append(normalized.tolist())
            else:
                embeddings.append(embedding_values)

        return embeddings

    async def get_embedding_dimension(self) -> int:
        """
        Get the dimensionality of embeddings from this model.

        Returns:
            Number of dimensions in embedding vectors
        """
        return self.output_dimensionality


def create_gemini_embedding_service(
    api_key: str,
    model: str = "gemini-embedding-001",
    output_dimensionality: int = 768,
    task_type: TaskType = "RETRIEVAL_DOCUMENT",
    batch_size: int = 100,
) -> GeminiEmbeddingService:
    """
    Convenience function to create a Gemini embedding service.

    Args:
        api_key: Google Gemini API key
        model: Embedding model to use
        output_dimensionality: Output dimensions (128-3072)
        task_type: Task type for optimization
        batch_size: Maximum texts per API call

    Returns:
        Configured GeminiEmbeddingService instance
    """
    return GeminiEmbeddingService(
        api_key=api_key,
        model=model,
        output_dimensionality=output_dimensionality,
        task_type=task_type,
        batch_size=batch_size,
    )
