import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import streamlit as st


# Initialize the embedding model
@st.cache_resource
def get_embedding_model():
    """Load the embedding model (cached for performance)"""
    return SentenceTransformer("all-MiniLM-L6-v2")


# Initialize or load ChromaDB
@st.cache_resource
def get_vector_db():
    """Initialize ChromaDB with persistence"""
    db_path = "data/chroma_db"
    os.makedirs(db_path, exist_ok=True)
    
    # Initialize persistent ChromaDB client
    client = chromadb.PersistentClient(path=db_path)
    
    # Get or create collection
    collection = client.get_or_create_collection(
        name="wikitext2",
        metadata={"hnsw:space": "cosine"}
    )
    
    return collection


def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks


def initialize_vector_db():
    """Initialize the vector database with dataset chunks"""
    collection = get_vector_db()
    
    # Check if already populated
    if collection.count() > 0:
        print(f"Vector DB already initialized with {collection.count()} documents")
        return collection
    
    print("Initializing vector database...")
    dataset_path = "data/dataset.txt"
    
    if not os.path.exists(dataset_path):
        print(f"Error: {dataset_path} not found. Please run 'python download_data.py' first.")
        return collection
    
    # Load and chunk the dataset
    with open(dataset_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    chunks = chunk_text(content, chunk_size=500, overlap=100)
    print(f"Created {len(chunks)} chunks from dataset")
    
    # Add chunks to the collection in batches
    batch_size = 100
    embedding_model = get_embedding_model()
    
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_ids = [f"doc_{i+j}" for j in range(len(batch_chunks))]
        
        # Generate embeddings for this batch
        embeddings = embedding_model.encode(batch_chunks)
        
        # Add to collection
        collection.add(
            ids=batch_ids,
            embeddings=embeddings,
            documents=batch_chunks,
            metadatas=[{"chunk_index": i+j} for j in range(len(batch_chunks))]
        )
        
        print(f"Added {i + len(batch_chunks)}/{len(chunks)} chunks")
    
    print(f"Vector DB initialized with {collection.count()} documents")
    return collection


def retrieve_documents(query, top_k=5):
    """Retrieve the most relevant documents for a query"""
    collection = get_vector_db()
    
    if collection.count() == 0:
        return [], []
    
    # Query the collection
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "distances"]
    )
    
    documents = results["documents"][0] if results["documents"] else []
    distances = results["distances"][0] if results["distances"] else []
    
    # Convert distances to similarity scores (cosine similarity)
    # Lower distance = higher similarity
    scores = [1 - d for d in distances]
    
    return documents, scores


def get_context_for_query(query, top_k=3):
    """Get formatted context string for a query"""
    documents, scores = retrieve_documents(query, top_k=top_k)
    
    if not documents:
        return "No relevant context found in the database."
    
    context_parts = []
    for i, (doc, score) in enumerate(zip(documents, scores), 1):
        context_parts.append(f"[Document {i} - Relevance: {score:.2f}]\n{doc}\n")
    
    return "\n".join(context_parts)
