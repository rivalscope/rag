import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api.api import api_router
from app.core.config import get_settings
from app.core.logging import setup_logging, get_logger
from app.core.exceptions import (
    LLMConnectionError,
    VectorDBConnectionError,
    MissingEnvironmentVariableError
)

# Setup logging first
setup_logging()
logger = get_logger()

# Load environment variables
load_dotenv()

# Load settings
settings = get_settings()

# Define lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    logger.info(f"Starting {settings.PROJECT_NAME} API server")
    yield
    # Shutdown event
    logger.info(f"Shutting down {settings.PROJECT_NAME} API server")

# Initialize the FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Add exception handlers
@app.exception_handler(LLMConnectionError)
@app.exception_handler(VectorDBConnectionError)
@app.exception_handler(MissingEnvironmentVariableError)
async def custom_exception_handler(request: Request, exc):
    logger.error(f"Exception occurred: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/")
def root():
    """Root endpoint for health check"""
    logger.info("Health check endpoint called")
    return {"status": "ok", "message": "RAG API is running"}

if __name__ == "__main__":
    # Run the application with uvicorn
    logger.info("Starting development server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)