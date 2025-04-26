import time
import asyncio
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
import json

from app.core.logging import get_logger
from app.schemas.rag import QuestionRequest
from app.services.retriever_service import RetrieverService
from app.services.rag_service import RagService

router = APIRouter()
logger = get_logger()

async def generate_stream_response(
    question: str, 
    retriever_service: RetrieverService,
    rag_service: RagService
) -> AsyncGenerator[str, None]:
    """
    Generate a streaming response for the question
    
    Args:
        question: The question to answer
        retriever_service: The retriever service
        rag_service: The RAG service
        
    Yields:
        JSON strings for tokens and metrics
    """
    try:
        # Start timing the entire process
        total_start_time = time.time()
        
        # Retrieve relevant documents
        vector_search_results, retrieval_time = retriever_service.retrieve(question)
        
        # Yield retrieval metrics
        yield json.dumps({
            "event": "retrieval_complete",
            "data": {
                "retrieval_time": retrieval_time
            }
        }) + "\n"
        
        # Generate streaming answer
        async for token_data in rag_service.generate_answer_stream(question, vector_search_results):
            # Each token_data already has the right format with token and possibly metrics
            yield json.dumps(token_data) + "\n"
            
            # Brief pause to ensure proper streaming behavior
            await asyncio.sleep(0)
        
        # Calculate and yield final metrics
        total_time = time.time() - total_start_time
        yield json.dumps({
            "event": "metrics",
            "data": {
                "total_processing_time": total_time
            }
        }) + "\n"
        
    except Exception as e:
        logger.error(f"Error in stream generation: {str(e)}", exc_info=True)
        yield json.dumps({
            "event": "error",
            "data": {
                "message": str(e)
            }
        }) + "\n"

@router.post("/answer/stream")
async def answer_question_stream(
    request: QuestionRequest,
    retriever_service: RetrieverService = Depends(lambda: RetrieverService()),
    rag_service: RagService = Depends(lambda: RagService())
):
    """
    Answer a question with streaming response
    """
    logger.info(f"Processing streaming question: '{request.question[:50]}...' (truncated)")
    
    return StreamingResponse(
        generate_stream_response(
            request.question, 
            retriever_service, 
            rag_service
        ),
        media_type="text/event-stream"
    )