import os
import sys
from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine, RouterQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.selectors import LLMSingleSelector, LLMMultiSelector
from llama_index.core import PropertyGraphIndex
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

def build_router():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set. The router requires an LLM to make routing decisions.")
        
    Settings.llm = OpenAI(model="gpt-4", temperature=0) # GPT-4 is highly recommended for reliable routing

    # --- 1. Setup SQL Query Engine (Phase 1) ---
    db_path = 'companies.db'
    if not os.path.exists(db_path):
        print("Error: companies.db not found. Run ingest_sql.py first.")
        return
        
    db_uri = f'sqlite:///file:{os.path.abspath(db_path)}?mode=ro'
    engine = create_engine(db_uri, connect_args={'uri': True})
    sql_database = SQLDatabase(engine, include_tables=['companies'])
    
    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["companies"]
    )
    
    # --- 2. Setup Graph Query Engine (Phase 2) ---
    print("Connecting to Neo4j Graph Store...")
    try:
        graph_store = Neo4jPropertyGraphStore(
            username="neo4j",
            password="password",
            url="bolt://localhost:7687",
        )
        graph_index = PropertyGraphIndex.from_existing(
            property_graph_store=graph_store
        )
        graph_query_engine = graph_index.as_query_engine(
            include_text=True,
            similarity_top_k=3
        )
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
        print("Ensure Neo4j is running. Cannot build router without Graph Engine.")
        return

    # --- 3. Wrap as Tools ---
    sql_tool = QueryEngineTool(
        query_engine=sql_query_engine,
        metadata=ToolMetadata(
            name="sql_financials_tool",
            description=(
                "Useful for translating natural language questions into SQL queries "
                "to get exact financial numbers, revenue, and sectors for companies. "
                "Use this strictly when the user asks for numbers, revenues, or tabular data."
            ),
        ),
    )
    
    graph_tool = QueryEngineTool(
        query_engine=graph_query_engine,
        metadata=ToolMetadata(
            name="graph_risks_competitors_tool",
            description=(
                "Useful for answering questions about company relationships, "
                "such as who a company competes with, who leads them, and what "
                "specific risks they face (e.g. supply chain, cybersecurity). "
                "Use this for non-numerical relationship questions."
            ),
        ),
    )

    # --- 4. Initialize Router ---
    print("Initializing Router Query Engine...")
    router_engine = RouterQueryEngine(
        selector=LLMSingleSelector.from_defaults(),
        query_engine_tools=[sql_tool, graph_tool],
        verbose=True
    )
    
    # --- 5. Test Queries ---
    questions = [
        "What is the revenue of Apple?",
        "Who does Microsoft compete with?",
        "Compare the revenue of companies facing supply chain risks."
    ]
    
    for q in questions:
        print(f"\n[Test Query] {q}")
        try:
            response = router_engine.query(q)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Query failed: {e}")

if __name__ == "__main__":
    build_router()
