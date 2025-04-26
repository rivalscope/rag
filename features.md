-should be able to select from db instead from .env llm model, embeddings model, vector db
-should be able to add and save prompt templates in a db
-should add as many inference engines deffinitions to connect to llms and save them in a db 
should add as many as possible vectors db server definitions to chat with them and add this in a db 


make one project that is just chat with the above characteristica
update this project as rag option with the above characteristics 

think about how to add more data sources to rag project mia mcp 

Prompt

RAG System Enhancement Prompt
Based on your project requirements, here's a detailed prompt for implementing the requested RAG system enhancements:

System Architecture Enhancement
"I need to enhance my RAG project with a modular architecture that supports:

Inference Engine & Model Registry:

Create a database schema to store LLM configurations
Each entry contains: unique identifier, inference engine type, model name, and API settings
Implement API endpoints for CRUD operations on these configurations
Embedding Model Registry:

Database schema for embedding models
Each entry with: unique identifier, embedding model type/name, and settings
CRUD API endpoints for embedding configurations
Data Source Registry:

Database schema to define vector stores and document sources
Each entry with: unique identifier, source type, connection parameters
CRUD API endpoints for data sources
Unified Inference Endpoint:

Create a flexible endpoint that accepts:
Input query/message
LLM identifier (references saved configuration)
Embedding model identifier (references saved configuration)
Data source identifier (references saved configuration)
The endpoint should dynamically configure the RAG pipeline based on these identifiers
Prompt Template Registry:

Schema for storing reusable prompt templates
CRUD endpoints for managing templates
Integration with inference endpoint
All configurations should be stored in SQLite. The system should provide a clean API interface where users can:

Define and save components with unique identifiers
Use those identifiers at inference time to dynamically configure the RAG pipeline"
This approach keeps the core RAG functionality while making it fully configurable through database-stored components.