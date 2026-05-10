#!/usr/bin/env python3
"""
Initialize the vector database for BasicRAG pipeline.
Run this script once after downloading the dataset:
  python download_data.py
  python setup_vector_db.py
"""

import os
from pipelines.vector_db import initialize_vector_db

def main():
    print("=" * 60)
    print("NexusRAG Vector Database Initialization")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists("data/dataset.txt"):
        print("\n❌ Error: data/dataset.txt not found!")
        print("   Please run: python download_data.py")
        print("   Then run this script again.")
        return
    
    print("\n📦 Initializing vector database...")
    initialize_vector_db()
    print("\n✅ Vector database initialization complete!")
    print("   You can now run: streamlit run app.py")

if __name__ == "__main__":
    main()
