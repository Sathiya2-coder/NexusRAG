#!/usr/bin/env python3
"""
Load text data into TigerGraph for GraphRAG
"""
import sys
import os
sys.path.insert(0, os.path.abspath("."))

from pyTigerGraph import TigerGraphConnection
import json

# TigerGraph Configuration
config = {
    "host": "https://tg-d30aafa4-669c-4606-b227-ae7da842e211.tg-3452941248.i.tgcloud.io",
    "username": "sathiya",
    "password": "Mano@2611",
    "graphname": "NexusRAG",
    "tgCloud": True
}

def connect_to_tigergraph():
    """Connect to TigerGraph instance"""
    print("Connecting to TigerGraph...")
    try:
        conn = TigerGraphConnection(
            host=config["host"],
            username=config["username"],
            password=config["password"],
            graphname=config["graphname"],
            tgCloud=config["tgCloud"]
        )
        print(f"✓ Connected to {config['graphname']}")
        return conn
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        sys.exit(1)

def load_documents_from_file(conn, filepath):
    """Load documents from a text file"""
    print(f"\nLoading documents from {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into documents (you can adjust this logic)
        documents = content.split('\n\n')  # Split by double newline
        documents = [doc.strip() for doc in documents if doc.strip()]
        
        print(f"Found {len(documents)} documents")
        
        # You can now ingest these documents into the graph
        # This depends on your graph schema
        print(f"✓ Loaded {len(documents)} documents")
        return documents
    
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        sys.exit(1)

def main():
    """Main function"""
    conn = connect_to_tigergraph()
    
    # Load from your dataset
    dataset_path = "data/dataset.txt"
    if os.path.exists(dataset_path):
        documents = load_documents_from_file(conn, dataset_path)
        print(f"\n✓ Ready to ingest {len(documents)} documents into GraphRAG")
    else:
        print(f"\n⚠️  Dataset not found at {dataset_path}")
        print("   Place your text data there and run again")

if __name__ == "__main__":
    main()
