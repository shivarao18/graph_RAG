import os
import sys
from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings

def test_query():
    # Setup database connection
    db_path = 'companies.db'
    if not os.path.exists(db_path):
        print(f"Error: Database {db_path} not found. Run ingest_sql.py first.")
        sys.exit(1)
        
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Initialize SQLDatabase wrapper from LlamaIndex
    sql_database = SQLDatabase(engine, include_tables=['companies'])
    
    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("LlamaIndex requires an LLM to translate natural language to SQL.")
        print("Please set your OPENAI_API_KEY, e.g.:")
        print("export OPENAI_API_KEY='sk-...'")
        print("For this test, we will attempt to proceed, but it will likely fail without a key.")
    
    # Initialize the query engine
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["companies"]
    )
    
    # Unit Test Query
    question = "What is Apple's revenue?"
    print(f"\n--- Testing Semantic Layer ---")
    print(f"Question: {question}")
    
    try:
        response = query_engine.query(question)
        print("\nGenerated SQL Query:")
        print(response.metadata.get('sql_query', 'No SQL Query found in metadata'))
        print("\nResponse:")
        print(response)
    except Exception as e:
        print(f"\nError executing query: {e}")
        print("If this is an authentication error, make sure your OPENAI_API_KEY is valid.")

if __name__ == "__main__":
    test_query()
