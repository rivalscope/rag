from fastapi import APIRouter

from app.api.endpoints import rag, rag_stream

api_router = APIRouter()

# Include all endpoint routers here
api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
api_router.include_router(rag_stream.router, prefix="/rag", tags=["rag-stream"])