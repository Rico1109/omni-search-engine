from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file explicitly (pydantic-settings v2 doesn't auto-load)
load_dotenv()


class EmbeddingSettings(BaseModel):
    # Provider selection: "openai" or "gemini"
    provider: str = Field("openai", alias="EMBEDDING_PROVIDER")
    
    # OpenAI settings
    openai_api_key: str = Field("", alias="OPENAI_API_KEY")
    
    # Gemini settings
    gemini_api_key: str = Field("", alias="GEMINI_API_KEY")
    gemini_model: str = Field("gemini-embedding-001", alias="GEMINI_MODEL")
    
    # Common settings
    model: str = Field("text-embedding-3-small", alias="EMBEDDING_MODEL")
    batch_size: int = Field(100, alias="EMBEDDING_BATCH_SIZE")
    output_dimensionality: int = Field(768, alias="EMBEDDING_DIMENSIONS")
    task_type: str = Field("RETRIEVAL_DOCUMENT", alias="EMBEDDING_TASK_TYPE")


class ChunkingSettings(BaseModel):
    target_chunk_size: int = Field(1000, alias="TARGET_CHUNK_SIZE")
    max_chunk_size: int = Field(2000, alias="MAX_CHUNK_SIZE")
    min_chunk_size: int = Field(100, alias="MIN_CHUNK_SIZE")


class RerankSettings(BaseModel):
    model: str = Field("ms-marco-TinyBERT-L-2-v2", alias="RERANK_MODEL")
    enabled: bool = Field(True, alias="RERANK_ENABLED")


class Settings(BaseSettings):
    obsidian_vault_path: Path = Field(..., alias="OBSIDIAN_VAULT_PATH")
    chromadb_path: Path = Field(Path("chroma_db"), alias="CHROMADB_PATH")

    embedding: EmbeddingSettings = Field(default=None)
    chunking: ChunkingSettings = Field(default=None)
    rerank: RerankSettings = Field(default=None)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode='before')
    @classmethod
    def build_nested_settings(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Construct nested settings from environment variables."""
        import os
        
        # Build EmbeddingSettings
        if 'embedding' not in data or data['embedding'] is None:
            data['embedding'] = EmbeddingSettings(
                EMBEDDING_PROVIDER=os.getenv('EMBEDDING_PROVIDER', data.get('embedding_provider', data.get('EMBEDDING_PROVIDER', 'openai'))),
                OPENAI_API_KEY=os.getenv('OPENAI_API_KEY', data.get('openai_api_key', data.get('OPENAI_API_KEY', ''))),
                GEMINI_API_KEY=os.getenv('GEMINI_API_KEY', data.get('gemini_api_key', data.get('GEMINI_API_KEY', ''))),
                GEMINI_MODEL=os.getenv('GEMINI_MODEL', data.get('gemini_model', data.get('GEMINI_MODEL', 'gemini-embedding-001'))),
                EMBEDDING_MODEL=os.getenv('EMBEDDING_MODEL', data.get('embedding_model', data.get('EMBEDDING_MODEL', 'text-embedding-3-small'))),
                EMBEDDING_BATCH_SIZE=int(os.getenv('EMBEDDING_BATCH_SIZE', data.get('embedding_batch_size', data.get('EMBEDDING_BATCH_SIZE', 100)))),
                EMBEDDING_DIMENSIONS=int(os.getenv('EMBEDDING_DIMENSIONS', data.get('embedding_dimensions', data.get('EMBEDDING_DIMENSIONS', 768)))),
                EMBEDDING_TASK_TYPE=os.getenv('EMBEDDING_TASK_TYPE', data.get('embedding_task_type', data.get('EMBEDDING_TASK_TYPE', 'RETRIEVAL_DOCUMENT')))
            )

        # Build ChunkingSettings
        if 'chunking' not in data or data['chunking'] is None:
            data['chunking'] = ChunkingSettings(
                TARGET_CHUNK_SIZE=int(os.getenv('TARGET_CHUNK_SIZE', data.get('target_chunk_size', data.get('TARGET_CHUNK_SIZE', 1000)))),
                MAX_CHUNK_SIZE=int(os.getenv('MAX_CHUNK_SIZE', data.get('max_chunk_size', data.get('MAX_CHUNK_SIZE', 2000)))),
                MIN_CHUNK_SIZE=int(os.getenv('MIN_CHUNK_SIZE', data.get('min_chunk_size', data.get('MIN_CHUNK_SIZE', 100))))
            )

        # Build RerankSettings
        if 'rerank' not in data or data['rerank'] is None:
            rerank_enabled = os.getenv('RERANK_ENABLED', data.get('rerank_enabled', data.get('RERANK_ENABLED', 'True')))
            if isinstance(rerank_enabled, str):
                rerank_enabled = rerank_enabled.lower() in ('true', '1', 'yes')
            data['rerank'] = RerankSettings(
                RERANK_MODEL=os.getenv('RERANK_MODEL', data.get('rerank_model', data.get('RERANK_MODEL', 'ms-marco-TinyBERT-L-2-v2'))),
                RERANK_ENABLED=rerank_enabled
            )

        return data


def get_settings() -> Settings:
    return Settings()
