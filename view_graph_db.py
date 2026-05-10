#!/usr/bin/env python3
"""
View and query the knowledge graph database.
"""

from pipelines.graph_db import (
    initialize_knowledge_graph,
    get_graph_statistics,
    traverse_graph_for_context,
    get_graph_context_for_query
)

def main():
    print("=" * 70)
    print("Knowledge Graph Viewer")
    print("=" * 70)
    
    graph = initialize_knowledge_graph()
    stats = get_graph_statistics()
    
    print(f"\n✅ Graph Status: {stats['status']}")
    print(f"   • Entities (Nodes): {stats['nodes']}")
    print(f"   • Relationships (Edges): {stats['edges']}")
    print(f"   • Graph Density: {stats['density']:.4f}")
    print(f"   • Average Node Degree: {stats['avg_degree']:.2f}")
    
    if stats["nodes"] == 0:
        print("\n❌ Knowledge graph is empty. Run 'python setup_graph_db.py' first.")
        return
    
    print("\n" + "=" * 70)
    print("TOP ENTITIES (by connections):")
    print("=" * 70)
    
    # Show top entities by degree
    degrees = dict(graph.degree())
    top_entities = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    
    for i, (entity, degree) in enumerate(top_entities, 1):
        print(f"{i:2d}. {entity:40s} - {degree:3d} connections")
    
    print("\n" + "=" * 70)
    print("SEARCH EXAMPLES:")
    print("=" * 70)
    
    # Example queries
    queries = [
        "What are the main historical topics?",
        "Find connections between major entities",
        "What topics are most connected?"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        context = get_graph_context_for_query(query, max_hops=2)
        lines = context.split('\n')
        # Show first few lines of context
        for line in lines[:5]:
            print(f"   {line}")
        if len(lines) > 5:
            print(f"   ... ({len(lines) - 5} more lines)")
    
    print("\n" + "=" * 70)
    print("INTERACTIVE QUERY:")
    print("=" * 70)
    
    while True:
        user_query = input("\nEnter a query (or 'quit' to exit): ").strip()
        if user_query.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_query:
            continue
        
        print(f"\n🔗 Graph traversal results:")
        context = get_graph_context_for_query(user_query, max_hops=2)
        print(context)

if __name__ == "__main__":
    main()
