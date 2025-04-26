import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings managed through environment variables"""
    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RAG API"
    
    # LLM settings
    OLLAMA_LLM_MODEL: str
    OLLAMA_LLM_BASE_URL: str
    
    # Embedding settings
    OLLAMA_EMBEDDING_MODEL: str
    OLLAMA_EMBEDDING_BASE_URL: str
    
    # Vector database settings
    CHROMA_DB_URL: str
    
    # RAG settings
    TOP_K_RESULTS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """Get cached settings to avoid loading from environment for every request"""
    return Settings()