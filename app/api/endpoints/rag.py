import time
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.logging import get_logger
from app.schemas.rag import QuestionRequest, QAResponse, MetricsResponse
from app.services.retriever_service import RetrieverService
from app.services.rag_service import RagService

router = APIRouter()
logger = get_logger()

@router.post("/answer", response_model=QAResponse)
async def answer_question(
    request: QuestionRequest,
    retriever_service: RetrieverService = Depends(lambda: RetrieverService()),
    rag_service: RagService = Depends(lambda: RagService())
):
    """
    Answer a question based on retrieved document contexts
    """
    try:
        logger.info(f"Processing question: '{request.question[:50]}...' (truncated)")
        
        # Start timing the entire process
        total_start_time = time.time()

        # Retrieve relevant documents
        logger.debug("Starting document retrieval")
        vector_search_results, retrieval_time = retriever_service.retrieve(request.question)
        logger.debug(f"Document retrieval completed in {retrieval_time:.3f}s")

        # Generate answer based on retrieved documents
        logger.debug("Starting answer generation")
        generation_result = rag_service.generate_answer(
            question=request.question,
            vector_search_results=vector_search_results
        )
        logger.debug(f"Answer generation completed in {generation_result['metrics']['total_generation_time']:.3f}s")

        # Calculate total processing time
        total_time = time.time() - total_start_time
        logger.info(f"Question answered in {total_time:.3f}s")

        # Create the response
        metrics = MetricsResponse(
            retrieval_time=retrieval_time,
            time_to_first_token=generation_result["metrics"]["time_to_first_token"],
            total_generation_time=generation_result["metrics"]["total_generation_time"],
            tokens=generation_result["metrics"]["tokens"],
            tokens_per_second=generation_result["metrics"]["tokens_per_second"],
            total_processing_time=total_time
        )
        
        return QAResponse(
            answer=generation_result["answer"],
            metrics=metrics
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )