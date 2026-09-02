# Corporate Intelligence Engine

## Objective
Build a financial RAG pipeline that routes natural language queries to the appropriate database based on the required context.

## Architecture
This project uses three data layers to process SEC 10-K filings and S&P 500 metrics:
1. **Semantic Layer (Cube / SQL):** Handles exact quantitative data (e.g., Revenue, Market Cap) via a structured PostgreSQL database.
2. **Knowledge Graph (Neo4j):** Maps qualitative entity relationships (e.g., Company -> [COMPETES_WITH] -> Company) extracted from SEC PDFs.
3. **GraphRAG Orchestrator (LlamaIndex):** Uses a large language model to parse the user's intent and route the query to either the Semantic API, the Graph DB, or a Vector Search.

## Learning Goals
* Understand how to configure LlamaIndex `PropertyGraphIndex`.
* Learn how to define metrics in a Cube semantic layer.
* Observe how the LLM decides between querying a graph vs. querying a SQL database.