#!/usr/bin/env python3
"""
Initialize the knowledge graph database for GraphRAG pipeline.
Run this script once after downloading the dataset:
  python download_data.py
  python setup_vector_db.py
  python setup_graph_db.py
"""

import os
from pipelines.graph_db import build_knowledge_graph_from_dataset, get_graph_statistics

def main():
    print("=" * 60)
    print("NexusRAG Knowledge Graph Initialization")
    print("=" * 60)
    
    # Check if dataset exists
    if not os.path.exists("data/dataset.txt"):
        print("\n❌ Error: data/dataset.txt not found!")
        print("   Please run: python download_data.py")
        print("   Then run this script again.")
        return
    
    print("\n🔗 Building knowledge graph...")
    build_knowledge_graph_from_dataset()
    
    # Show statistics
    stats = get_graph_statistics()
    
    print("\n" + "=" * 60)
    print("✅ Knowledge Graph Initialization Complete!")
    print("=" * 60)
    print(f"\n📊 Graph Statistics:")
    print(f"   • Entities (Nodes): {stats['nodes']}")
    print(f"   • Relationships (Edges): {stats['edges']}")
    print(f"   • Graph Density: {stats['density']:.4f}")
    print(f"   • Average Degree: {stats['avg_degree']:.2f}")
    
    print(f"\n✅ You can now run: streamlit run app.py")

if __name__ == "__main__":
    main()
