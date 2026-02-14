from functools import lru_cache

from crawlers.markdown_crawler import MarkdownChunker
from repositories.snippet_repository import VectorStore
from services.embedding_service import EmbeddingService
from services.gemini_embedding_service import GeminiEmbeddingService
from services.indexer_service import VaultIndexer
from services.rerank_service import RerankService
from settings import get_settings


@lru_cache
def get_rerank_service() -> RerankService:
    settings = get_settings()
    return RerankService(
        model_name=settings.rerank.model,
        enabled=settings.rerank.enabled
    )


@lru_cache
def get_vector_store() -> VectorStore:
    settings = get_settings()
    return VectorStore(
        persist_directory=str(settings.chromadb_path), collection_name="obsidian_notes"
    )


@lru_cache
def get_embedding_service() -> EmbeddingService | GeminiEmbeddingService:
    settings = get_settings()
    provider = settings.embedding.provider.lower()
    
    if provider == "gemini":
        return GeminiEmbeddingService(
            api_key=settings.embedding.gemini_api_key,
            model=settings.embedding.gemini_model,
            output_dimensionality=settings.embedding.output_dimensionality,
            task_type=settings.embedding.task_type,
            batch_size=settings.embedding.batch_size,
        )
    elif provider == "openai":
        return EmbeddingService(
            api_key=settings.embedding.openai_api_key,
            model=settings.embedding.model,
            batch_size=settings.embedding.batch_size,
        )
    else:
        raise ValueError(
            f"Unsupported embedding provider: {provider}. "
            f"Supported providers: 'openai', 'gemini'"
        )


@lru_cache
def get_chunker() -> MarkdownChunker:
    settings = get_settings()
    return MarkdownChunker(
        target_chunk_size=settings.chunking.target_chunk_size,
        max_chunk_size=settings.chunking.max_chunk_size,
        min_chunk_size=settings.chunking.min_chunk_size,
    )


@lru_cache
def get_indexer() -> VaultIndexer:
    settings = get_settings()
    return VaultIndexer(
        vault_path=settings.obsidian_vault_path,
        vector_store=get_vector_store(),
        embedding_service=get_embedding_service(),
        chunker=get_chunker(),
    )


def get_fresh_indexer() -> VaultIndexer:
    """
    Create a new VaultIndexer instance with its own EmbeddingService.
    Useful for background threads (Watcher) to avoid sharing async clients across loops.
    """
    settings = get_settings()
    provider = settings.embedding.provider.lower()
    
    # Create fresh embedding service based on provider
    if provider == "gemini":
        fresh_embedding_service = GeminiEmbeddingService(
            api_key=settings.embedding.gemini_api_key,
            model=settings.embedding.gemini_model,
            output_dimensionality=settings.embedding.output_dimensionality,
            task_type=settings.embedding.task_type,
            batch_size=settings.embedding.batch_size,
        )
    elif provider == "openai":
        fresh_embedding_service = EmbeddingService(
            api_key=settings.embedding.openai_api_key,
            model=settings.embedding.model,
            batch_size=settings.embedding.batch_size,
        )
    else:
        raise ValueError(
            f"Unsupported embedding provider: {provider}. "
            f"Supported providers: 'openai', 'gemini'"
        )

    return VaultIndexer(
        vault_path=settings.obsidian_vault_path,
        vector_store=get_vector_store(),
        embedding_service=fresh_embedding_service,
        chunker=get_chunker(),
    )
