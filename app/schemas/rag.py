from pydantic import BaseModel, Field

class QuestionRequest(BaseModel):
    """Schema for question request"""
    question: str = Field(..., description="The question to be answered based on the documents")

class MetricsResponse(BaseModel):
    """Schema for timing metrics in the response"""
    retrieval_time: float = Field(..., description="Time taken to retrieve documents in seconds")
    time_to_first_token: float = Field(..., description="Time to first token in seconds")
    total_generation_time: float = Field(..., description="Total time for response generation in seconds")
    tokens: int = Field(..., description="Number of tokens generated")
    tokens_per_second: float = Field(..., description="Token generation speed in tokens per second")
    total_processing_time: float = Field(..., description="Total processing time in seconds")

class QAResponse(BaseModel):
    """Schema for question answering response"""
    answer: str = Field(..., description="The generated answer to the question")
    metrics: MetricsResponse = Field(..., description="Performance metrics for the response")