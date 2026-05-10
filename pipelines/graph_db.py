import os
import pickle
import json
import re
from collections import defaultdict
import networkx as nx
import streamlit as st


def get_graph_path():
    """Get the path for storing the knowledge graph"""
    graph_path = "data/knowledge_graph.pkl"
    return graph_path


@st.cache_resource
def initialize_knowledge_graph():
    """Initialize or load the knowledge graph"""
    graph_path = get_graph_path()
    
    if os.path.exists(graph_path):
        with open(graph_path, 'rb') as f:
            graph = pickle.load(f)
        print(f"Loaded existing knowledge graph with {graph.number_of_nodes()} nodes and {graph.number_of_edges()} edges")
        return graph
    
    print("Creating new knowledge graph...")
    graph = nx.DiGraph()
    return graph


def extract_entities_and_relationships(text, chunk_id):
    """
    Extract entities and relationships from text using pattern matching.
    Optimized to process entire text efficiently.
    """
    entities = []
    relationships = []
    
    # Process full text for complete coverage
    words = text.split()
    
    # Extract all entities (capitalized words, numbers, dates)
    for i, word in enumerate(words):
        if word and len(word) > 2 and (word[0].isupper() or re.match(r'\d+', word)):
            context_start = max(0, i - 1)
            context_end = min(len(words), i + 2)
            phrase = " ".join(words[context_start:context_end]).strip()
            
            if len(phrase) > 3 and len(phrase) < 100 and phrase not in entities:
                entities.append(phrase)
    
    # Extract relationships - simple patterns (process entire text)
    patterns = [
        (r'(\w+(?:\s+\w+)*?)\s+is\s+(?:a\s+)?(\w+(?:\s+\w+)*?)', 'is_type_of'),
        (r'(\w+(?:\s+\w+)*?)\s+(?:has|contains|includes)\s+(\w+(?:\s+\w+)*?)', 'has'),
        (r'(\w+(?:\s+\w+)*?)\s+(?:related|connected)\s+to\s+(\w+(?:\s+\w+)*?)', 'related_to'),
        (r'(\w+(?:\s+\w+)*?)\s+and\s+(\w+(?:\s+\w+)*?)\s+are', 'co_occurs'),
    ]
    
    for pattern, rel_type in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            entity1 = match.group(1).strip()
            entity2 = match.group(2).strip()
            if entity1 and entity2 and len(entity1) > 2 and len(entity2) > 2 and len(entity1) < 100 and len(entity2) < 100:
                relationships.append({
                    'source': entity1,
                    'target': entity2,
                    'type': rel_type,
                    'chunk_id': chunk_id
                })
    
    return entities, relationships


def build_knowledge_graph_from_dataset():
    """Build knowledge graph from the ENTIRE dataset"""
    dataset_path = "data/dataset.txt"
    graph_path = get_graph_path()
    
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found")
        return None
    
    graph = nx.DiGraph()
    
    print("Building knowledge graph from ENTIRE dataset...")
    
    with open(dataset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by sentences/lines for better chunking
    chunks = [line.strip() for line in content.split('\n') if line.strip()]
    
    total_chunks = len(chunks)
    print(f"Processing ALL {total_chunks} chunks from dataset...")
    
    for chunk_id, chunk in enumerate(chunks):
        if not chunk or len(chunk) < 5:
            continue
        
        # Progress indicator every 500 chunks
        if (chunk_id + 1) % 500 == 0:
            print(f"  ✓ Processed {chunk_id + 1}/{total_chunks} chunks...")
        
        entities, relationships = extract_entities_and_relationships(chunk, chunk_id)
        
        # Add entities as nodes
        for entity in entities:
            if entity not in graph:
                graph.add_node(entity, type='entity', chunk_id=chunk_id)
        
        # Add relationships as edges
        for rel in relationships:
            source = rel['source']
            target = rel['target']
            rel_type = rel['type']
            
            # Ensure nodes exist
            if source not in graph:
                graph.add_node(source, type='entity', chunk_id=chunk_id)
            if target not in graph:
                graph.add_node(target, type='entity', chunk_id=chunk_id)
            
            # Add edge with relationship type (avoid duplicates)
            if not graph.has_edge(source, target):
                graph.add_edge(source, target, relation=rel_type, chunk_id=chunk_id)
    
    # Save the graph
    os.makedirs(os.path.dirname(graph_path), exist_ok=True)
    with open(graph_path, 'wb') as f:
        pickle.dump(graph, f)
    
    print(f"\n✅ Knowledge graph built successfully!")
    print(f"   • Chunks processed: {total_chunks}")
    print(f"   • Total entities: {graph.number_of_nodes()}")
    print(f"   • Total relationships: {graph.number_of_edges()}")
    return graph


def find_path_between_entities(graph, source, target, max_hops=3):
    """Find shortest path between two entities in the graph"""
    try:
        path = nx.shortest_path(graph, source, target, cutoff=max_hops)
        return path
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


def traverse_graph_for_context(graph, query, max_depth=2):
    """
    Traverse the knowledge graph to find relevant context for a query.
    Extract entities from query and find related nodes.
    """
    if not graph or len(graph) == 0:
        return []
    
    # Simple entity extraction from query
    query_words = query.split()
    relevant_nodes = []
    context_edges = []
    
    # Find nodes that match query terms (case-insensitive)
    for node in graph.nodes():
        for word in query_words:
            if len(word) > 3 and word.lower() in node.lower():
                relevant_nodes.append(node)
                break
    
    # If no exact matches, take random high-degree nodes
    if not relevant_nodes:
        if graph.number_of_nodes() > 0:
            degrees = dict(graph.degree())
            top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            relevant_nodes = [node for node, _ in top_nodes]
    
    # Traverse from relevant nodes
    visited = set()
    context_graph = nx.DiGraph()
    
    def traverse(node, depth):
        if depth > max_depth or node in visited:
            return
        visited.add(node)
        context_graph.add_node(node, **graph.nodes[node])
        
        # Add successors
        for successor in graph.successors(node):
            edge_data = graph.get_edge_data(node, successor)
            context_graph.add_edge(node, successor, **edge_data)
            if depth < max_depth - 1:
                traverse(successor, depth + 1)
        
        # Add predecessors
        for predecessor in graph.predecessors(node):
            edge_data = graph.get_edge_data(predecessor, node)
            context_graph.add_edge(predecessor, node, **edge_data)
            if depth < max_depth - 1:
                traverse(predecessor, depth + 1)
    
    # Traverse from relevant nodes
    for node in relevant_nodes[:3]:  # Limit to 3 starting nodes
        traverse(node, 0)
    
    return context_graph


def get_graph_context_for_query(query, max_hops=2):
    """Get context from the knowledge graph for a query"""
    graph = initialize_knowledge_graph()
    
    if graph.number_of_nodes() == 0:
        return "Knowledge graph is empty. Run 'python setup_graph_db.py' to build it."
    
    context_graph = traverse_graph_for_context(graph, query, max_depth=max_hops)
    
    if context_graph.number_of_nodes() == 0:
        return "No relevant context found in the knowledge graph."
    
    # Format the graph context
    context_parts = []
    context_parts.append(f"Knowledge Graph Context (Entities: {context_graph.number_of_nodes()}, Relations: {context_graph.number_of_edges()})")
    context_parts.append("-" * 60)
    
    # Show entities and their relationships
    for node in list(context_graph.nodes())[:10]:  # Limit to 10 nodes
        outgoing = list(context_graph.successors(node))
        if outgoing:
            relationships_str = ", ".join(outgoing[:3])
            context_parts.append(f"• {node} → {relationships_str}")
    
    context_parts.append("-" * 60)
    context_parts.append(f"Total entities in traversal: {context_graph.number_of_nodes()}")
    context_parts.append(f"Total relationships found: {context_graph.number_of_edges()}")
    
    return "\n".join(context_parts)


def get_graph_statistics():
    """Get statistics about the knowledge graph"""
    graph = initialize_knowledge_graph()
    
    if graph.number_of_nodes() == 0:
        return {"status": "empty", "nodes": 0, "edges": 0}
    
    stats = {
        "status": "ready",
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": nx.density(graph),
        "avg_degree": sum(dict(graph.degree()).values()) / graph.number_of_nodes() if graph.number_of_nodes() > 0 else 0
    }
    
    return stats
