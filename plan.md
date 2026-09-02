# Implementation Blueprint: Corporate Intelligence Engine

## Phase 1: Environment & Semantic Layer
- [ ] Initialize a Python virtual environment and install dependencies (`llama-index`, `neo4j`, `pandas`, `sqlalchemy`).
- [ ] Create a local SQLite or PostgreSQL database.
- [ ] Write a script to ingest a mock Kaggle S&P 500 CSV (Ticker, Company, Revenue, Sector) into the SQL database.
- [ ] Configure a basic Semantic Layer interface (using Cube or a programmatic LlamaIndex SQL router) to define a `Revenue` metric.
- [ ] Write a unit test: Ask the system "What is Apple's revenue?" and assert it executes a SQL query.

## Phase 2: Knowledge Graph Ingestion
- [ ] Spin up a local Neo4j instance (via Docker or Neo4j Desktop).
- [ ] Download two SEC 10-K PDFs (e.g., Apple and Microsoft).
- [ ] Use LlamaIndex `SchemaLLMPathExtractor` to define the ontology: `Company`, `Person`, `RiskFactor`.
- [ ] Write the ingestion script to chunk the PDFs, extract triples, and load them into Neo4j.
- [ ] Write a Cypher query to verify nodes were created successfully.

## Phase 3: The GraphRAG Router
- [ ] Create a unified query engine in LlamaIndex.
- [ ] Add the SQL Semantic engine as a `QueryEngineTool`.
- [ ] Add the Neo4j Graph engine as a `QueryEngineTool`.
- [ ] Implement an LLM-based router that classifies incoming user questions and delegates them to the correct tool.
- [ ] Test with a cross-domain query: "Compare the revenue [SQL] of companies facing supply chain risks [Graph]."