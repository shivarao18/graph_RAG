import os
import sys
from llama_index.core import SimpleDirectoryReader, PropertyGraphIndex
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from typing import Literal

def ingest_knowledge_graph():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set. Extraction will fail.")

    Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0)

    print("Connecting to Neo4j on localhost:7687...")
    try:
        # Use Neo4j as the Graph Store
        graph_store = Neo4jPropertyGraphStore(
            username="neo4j",
            password="password",
            url="bolt://localhost:7687",
        )
    except Exception as e:
        print(f"Failed to connect to Neo4j. Make sure it is running on localhost:7687.\nError: {e}")
        return

    # Define our strict Ontology
    # Using SchemaLLMPathExtractor to restrict extraction to Company, Person, and RiskFactor
    extractor = SchemaLLMPathExtractor(
        llm=Settings.llm,
        possible_entities=Literal["Company", "Person", "RiskFactor"],
        possible_relations=Literal["FACES_RISK", "LED_BY", "COMPETES_WITH"],
        max_triplets_per_chunk=5
    )

    data_dir = 'sec_filings'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created {data_dir}/ directory. Please add your mock 10-K PDFs or text files there and re-run.")
        return

    documents = SimpleDirectoryReader(data_dir).load_data()
    if not documents:
        print(f"No files found in {data_dir}/. Add files and try again.")
        return

    print(f"Loaded {len(documents)} document(s). Starting extraction (this may take a while)...")
    
    # Build the Property Graph Index
    index = PropertyGraphIndex.from_documents(
        documents,
        kg_extractors=[extractor],
        property_graph_store=graph_store,
        show_progress=True,
    )
    
    print("Ingestion complete! Data loaded into Neo4j.")

    # Verify via Cypher
    print("\n--- Verifying Nodes with Cypher ---")
    try:
        query = "MATCH (n) RETURN labels(n) as Label, count(n) as Count"
        # Access the underlying neo4j driver to run a raw query
        records, summary, keys = graph_store.client.execute_query(query)
        print("Node Counts by Label:")
        for r in records:
            print(f"- {r['Label']}: {r['Count']}")
    except Exception as e:
        print(f"Error running Cypher verification query: {e}")

if __name__ == "__main__":
    ingest_knowledge_graph()
