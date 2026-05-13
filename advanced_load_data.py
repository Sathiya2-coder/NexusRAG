#!/usr/bin/env python3
"""
Advanced data loading into TigerGraph for GraphRAG using REST API
"""
import sys
import os
import json
import requests
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

# TigerGraph Configuration
TG_HOST = "https://tg-d30aafa4-669c-4606-b227-ae7da842e211.tg-3452941248.i.tgcloud.io"
TG_USERNAME = "sathiya"
TG_PASSWORD = "Mano@2611"
TG_GRAPH = "NexusRAG"
TG_REST_PORT = 9000

def count_tokens(text):
    """Rough token count (words / 1.3)"""
    return len(text.split()) // 1.3

def load_documents_chunked(filepath, chunk_size=1000):
    """Load documents and chunk them smartly"""
    print(f"\nLoading and chunking dataset from {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by article (= = Article Name = =)
        articles = content.split('= ')
        articles = [f'= {a}' for a in articles if a.strip()]
        
        print(f"Found {len(articles)} articles")
        
        # Further chunk large articles
        chunks = []
        for article in articles:
            # Split article by sentences
            sentences = article.split('.')
            current_chunk = []
            current_size = 0
            
            for sentence in sentences:
                sent_tokens = count_tokens(sentence)
                if current_size + sent_tokens > chunk_size and current_chunk:
                    chunks.append('. '.join(current_chunk) + '.')
                    current_chunk = []
                    current_size = 0
                
                current_chunk.append(sentence)
                current_size += sent_tokens
            
            if current_chunk:
                chunks.append('. '.join(current_chunk) + '.')
        
        # Calculate total tokens
        total_tokens = sum(count_tokens(chunk) for chunk in chunks)
        
        print(f"Created {len(chunks)} chunks")
        print(f"Total tokens (estimated): {int(total_tokens):,}")
        
        return chunks, total_tokens
    
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        sys.exit(1)

def ingest_documents(chunks):
    """Ingest documents via GraphRAG REST API"""
    print(f"\n{'='*50}")
    print(f"Ingesting {len(chunks)} documents into TigerGraph...")
    print(f"{'='*50}\n")
    
    # Document ingestion endpoint (GraphRAG container)
    # This depends on how GraphRAG is deployed
    
    ingested = 0
    for i, chunk in enumerate(chunks[:5], 1):  # Ingest first 5 for demo
        doc_id = f"doc_{i:04d}"
        print(f"[{i}/{min(5, len(chunks))}] Ingesting {doc_id}...")
        print(f"  Size: {len(chunk)} chars, ~{int(count_tokens(chunk))} tokens")
        
        # You would call the GraphRAG API here
        # For now, we're just showing the structure
        ingested += 1
    
    if len(chunks) > 5:
        print(f"\n... and {len(chunks) - 5} more documents")
        print(f"Total documents to ingest: {len(chunks)}")
    
    return ingested

def main():
    """Main function"""
    print("="*50)
    print("GraphRAG Data Loader")
    print("="*50)
    
    # Load and chunk data
    dataset_path = "data/dataset.txt"
    if not os.path.exists(dataset_path):
        print(f"✗ Dataset not found at {dataset_path}")
        sys.exit(1)
    
    chunks, total_tokens = load_documents_chunked(dataset_path, chunk_size=1000)
    
    # Ingest into TigerGraph
    ingested = ingest_documents(chunks)
    
    print(f"\n{'='*50}")
    print(f"✓ Ready to ingest {len(chunks)} documents")
    print(f"✓ Total tokens: {int(total_tokens):,}")
    print(f"{'='*50}")
    
    print("\n📝 Next Steps:")
    print("1. Go to TigerGraph Admin Portal")
    print(f"   URL: {TG_HOST}:14240")
    print("2. Select 'Load Data' for graph 'NexusRAG'")
    print("3. Upload data/dataset.txt")
    print("4. Configure mapping and load into graph")

if __name__ == "__main__":
    main()
