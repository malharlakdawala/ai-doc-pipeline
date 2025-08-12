"""Configuration for ai-doc-pipeline."""

import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    chroma_persist_dir: str = Field(default="./chroma_data", alias="CHROMA_PERSIST_DIR")
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")
    model: str = Field(default="claude-sonnet-4-20250514", alias="MODEL")
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")
    top_k: int = Field(default=5, alias="TOP_K")

    class Config:
        env_file = ".env"


settings = Config()
