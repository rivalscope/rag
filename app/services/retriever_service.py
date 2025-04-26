import time
from urllib.parse import urlparse

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import chromadb

from app.core.config import get_settings
from app.core.exceptions import VectorDBConnectionError, MissingEnvironmentVariableError

settings = get_settings()

class TimedRetriever:
    """A wrapper for the LangChain retriever that adds timing functionality"""
    def __init__(self, base_retriever):
        self.base_retriever = base_retriever

    def invoke(self, query):
        """
        Invoke the retriever and track timing
        
        Args:
            query (str): The query to search for
            
        Returns:
            The retrieved document contexts
        """
        # Start timing for embedding generation
        embedding_start_time = time.time()
        
        # Get results from the base retriever
        results = self.base_retriever.invoke(query)
        
        # Calculate embedding and retrieval time
        self.embedding_time = time.time() - embedding_start_time
        return results, self.embedding_time

class RetrieverService:
    """Service for document retrieval operations"""
    
    def __init__(self):
        """Initialize the retriever service with vector store connection"""
        self.vector_store = None
        self.retriever = None
        self._initialize_retriever()
        
    def _initialize_retriever(self):
        """Initialize connection to the vector database and create retriever"""
        # Check for required environment variables
        required_vars = ["OLLAMA_EMBEDDING_MODEL", "OLLAMA_EMBEDDING_BASE_URL", "CHROMA_DB_URL"]
        missing_vars = [var for var in required_vars if not getattr(settings, var, None)]
        if missing_vars:
            raise MissingEnvironmentVariableError(missing_vars)

        # Initialize embeddings model
        try:
            embeddings = OllamaEmbeddings(
                model=settings.OLLAMA_EMBEDDING_MODEL,
                base_url=settings.OLLAMA_EMBEDDING_BASE_URL
            )
        except Exception as e:
            raise VectorDBConnectionError(f"Error initializing Ollama embeddings: {str(e)}")

        # Parse the Chroma DB URL
        try:
            chroma_url = settings.CHROMA_DB_URL
            if not chroma_url.startswith("http"):
                chroma_url = f"http://{chroma_url}"
            
            parsed_url = urlparse(chroma_url)
            host = parsed_url.hostname or "localhost"
            port = parsed_url.port or 4555
        except Exception:
            host = "localhost"
            port = 4555

        # Connect to Chroma vector database
        try:
            # Create a direct HTTP client connection
            chroma_client = chromadb.HttpClient(
                host=host,
                port=port
            )
            
            # Test connection
            chroma_client.heartbeat()
            
            # Pass the client directly to Chroma
            self.vector_store = Chroma(
                collection_name="document_collection",
                client=chroma_client,
                embedding_function=embeddings
            )
        except Exception as e:
            raise VectorDBConnectionError(f"Error connecting to Chroma database: {str(e)}")

        # Create retriever with the specified top_k value
        base_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": settings.TOP_K_RESULTS}
        )

        # Wrap with the timed retriever
        self.retriever = TimedRetriever(base_retriever)
    
    def retrieve(self, query: str):
        """
        Retrieve relevant document contexts for a query
        
        Args:
            query (str): The user query to search for
            
        Returns:
            tuple: (retrieved_contexts, retrieval_time)
        """
        if not self.retriever:
            self._initialize_retriever()
            
        results, retrieval_time = self.retriever.invoke(query)
        return results, retrieval_time