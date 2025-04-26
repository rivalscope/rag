from fastapi import HTTPException, status

class LLMConnectionError(HTTPException):
    """Exception raised when there's an issue connecting to the LLM service"""
    def __init__(self, detail: str = "Could not connect to LLM service"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class VectorDBConnectionError(HTTPException):
    """Exception raised when there's an issue connecting to the vector database"""
    def __init__(self, detail: str = "Could not connect to vector database"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class MissingEnvironmentVariableError(HTTPException):
    """Exception raised when required environment variables are missing"""
    def __init__(self, missing_vars: list):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing required environment variables: {', '.join(missing_vars)}"
        )