# RAG API Service

A FastAPI-based Retrieval-Augmented Generation (RAG) service that provides AI-powered question answering by leveraging document retrieval from a vector database.

## Overview

This project implements a modern RAG architecture that combines:

1. Vector-based document retrieval from ChromaDB
2. LLM text generation using Ollama
3. FastAPI endpoints for efficient question answering

The system provides both synchronous and streaming API endpoints, with comprehensive metrics tracking.

## Features

- **Document Retrieval**: Uses ChromaDB as vector store and Ollama for embedding generation
- **LLM Integration**: Connects to Ollama for text generation with customizable prompt templates
- **Streaming Support**: Offers both standard and streaming API endpoints
- **Performance Metrics**: Tracks detailed metrics including time to first token, tokens per second, and retrieval time
- **Robust Error Handling**: Comprehensive error handling for LLM and database connections

## Architecture

```
/app
├── api/             # API endpoints
├── core/            # Core configuration and utilities
├── schemas/         # Pydantic models for request/response validation
└── services/        # Business logic services
```

### Key Components:

- **RetrieverService**: Manages document retrieval from ChromaDB using embeddings
- **RagService**: Handles LLM interaction and answer generation
- **API Endpoints**: Both standard and streaming endpoints for question answering

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd rag
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv _venv
   source _venv/bin/activate  # On Windows: _venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file with required variables:**
   ```
   # Ollama settings for LLM
   OLLAMA_LLM_MODEL=<model-name>
   OLLAMA_LLM_BASE_URL=http://localhost:11434
   
   # Ollama settings for embeddings
   OLLAMA_EMBEDDING_MODEL=<embedding-model-name>
   OLLAMA_EMBEDDING_BASE_URL=http://localhost:11434
   
   # ChromaDB settings
   CHROMA_DB_URL=http://localhost:4555
   
   # RAG settings
   TOP_K_RESULTS=5
   ```

5. **Start the service:**
   ```bash
   python main.py
   ```

## API Endpoints

### Standard Question Answering
`POST /api/v1/rag/answer`

Request:
```json
{
  "question": "Your question here"
}
```

Response:
```json
{
  "answer": "Generated answer based on retrieved documents",
  "metrics": {
    "retrieval_time": 0.123,
    "time_to_first_token": 0.456,
    "total_generation_time": 1.234,
    "tokens": 42,
    "tokens_per_second": 10.5,
    "total_processing_time": 1.357
  }
}
```

### Streaming Question Answering
`POST /api/v1/rag/stream`

Request: Same as standard endpoint

Response: Server-sent events stream with real-time tokens and metrics

## Dependencies

- **FastAPI**: Web framework for building APIs
- **Langchain**: Framework for LLM applications
- **ChromaDB**: Vector database for document storage and retrieval
- **Ollama**: Local LLM deployment

## Development

This project follows standard Python best practices. To contribute:

1. Create a feature branch
2. Make your changes
3. Run tests
4. Submit a pull request

## License

[Specify your license here]