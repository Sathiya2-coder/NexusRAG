#!/usr/bin/env python3
"""
View and query the vector database.
"""

import sys
from pipelines.vector_db import get_vector_db, retrieve_documents, get_context_for_query

def main():
    collection = get_vector_db()
    
    print("=" * 70)
    print("Vector Database Viewer")
    print("=" * 70)
    print(f"\n✅ Total Documents in DB: {collection.count()}")
    
    if collection.count() == 0:
        print("❌ Vector database is empty. Run 'python setup_vector_db.py' first.")
        return
    
    print("\n" + "=" * 70)
    print("SAMPLE DOCUMENTS (first 5):")
    print("=" * 70)
    
    # Get first 5 documents
    results = collection.get(limit=5, include=["documents", "metadatas"])
    
    for i, (doc_id, text, metadata) in enumerate(
        zip(results["ids"], results["documents"], results["metadatas"]), 1
    ):
        print(f"\n📄 Document {i} (ID: {doc_id})")
        print(f"   Chunk Index: {metadata.get('chunk_index', 'N/A')}")
        print(f"   Preview: {text[:150]}...")
    
    print("\n" + "=" * 70)
    print("SEARCH EXAMPLES:")
    print("=" * 70)
    
    # Example queries
    queries = [
        "history of technology",
        "ancient civilizations",
        "scientific discoveries"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        documents, scores = retrieve_documents(query, top_k=2)
        
        for j, (doc, score) in enumerate(zip(documents, scores), 1):
            print(f"   Result {j} (Relevance: {score:.2f})")
            print(f"   {doc[:100]}...")
    
    print("\n" + "=" * 70)
    print("To search for your own query, use:")
    print("=" * 70)
    print("""
from pipelines.vector_db import get_context_for_query

context = get_context_for_query("your search query here", top_k=3)
print(context)
""")

if __name__ == "__main__":
    main()
