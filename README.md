# Corporate Intelligence Engine (Agentic GraphRAG)

An advanced Agentic Retrieval-Augmented Generation (RAG) system built with LlamaIndex. This project combines a traditional SQL database (for exact numerical/financial data) with a Knowledge Graph (for unstructured relationships and risks), orchestrated by an LLM Router.

## Architecture

This project is divided into three distinct phases:

### Phase 1: Semantic Layer & SQL Database
- **Files**: `ingest_sql.py`, `query_sql.py`
- **Description**: Sets up a local SQLite database (`companies.db`) containing mock S&P 500 tabular data. Uses LlamaIndex's `NLSQLTableQueryEngine` as a semantic layer to translate natural language into deterministic SQL queries securely via read-only connections.

### Phase 2: Knowledge Graph Ingestion
- **Files**: `ingest_graph.py`, `sec_filings/`
- **Description**: Uses a strict ontology (`Company`, `Person`, `RiskFactor`) and a `SchemaLLMPathExtractor` to parse unstructured SEC 10-K text. Triples are extracted and ingested into a local Neo4j graph database.

### Phase 3: The LLM Router
- **Files**: `router.py`
- **Description**: Wraps the SQL Engine and Graph Engine into abstract Tools. Uses an `LLMSingleSelector` Router to dynamically evaluate the intent of a user query and route it to the optimal database tool.

## Interactive Blueprint
An interactive Mermaid.js diagram of the system flow is available. Open `architecture.html` in any web browser to view the architecture boundary map.

---

## Setup Instructions

1. **Clone and create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install llama-index neo4j pandas sqlalchemy llama-index-graph-stores-neo4j
   ```

2. **Environment Variables**:
   You must set your OpenAI API key for the LLM extraction and routing to work:
   ```bash
   export OPENAI_API_KEY='your-api-key'
   ```

3. **Neo4j Setup**:
   Ensure Neo4j is running locally (e.g., via Neo4j Desktop or Docker) with the APOC plugin enabled on `bolt://localhost:7687`.
   Default credentials in code: `neo4j` / `password`.

4. **Running the Pipeline**:
   - `python3 ingest_sql.py` - Builds the structured SQLite database.
   - `python3 ingest_graph.py` - Builds the Neo4j knowledge graph from SEC filings.
   - `python3 router.py` - Runs the agentic router testing both tools and cross-domain questions.
