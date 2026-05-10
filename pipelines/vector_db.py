import os
import sys
from sentence_transformers import SentenceTransformer
import streamlit as st

# Try to import chromadb, but make it optional
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except (ImportError, AttributeError) as e:
    print(f"Warning: ChromaDB not available: {e}")
    CHROMADB_AVAILABLE = False
    chromadb = None


# Initialize the embedding model
@st.cache_resource
def get_embedding_model():
    """Load the embedding model (cached for performance)"""
    return SentenceTransformer("all-MiniLM-L6-v2")


# Initialize or load ChromaDB
@st.cache_resource
def get_vector_db():
    """Initialize ChromaDB with persistence"""
    if not CHROMADB_AVAILABLE:
        print("ChromaDB not available - returning None")
        return None
    
    try:
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
    except Exception as e:
        print(f"Error initializing ChromaDB: {e}")
        return None


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
    try:
        collection = get_vector_db()
        
        if collection is None:
            print("Vector DB collection is None - skipping initialization")
            return None
        
        # Check if already populated
        if collection.count() > 0:
            print(f"Vector DB already initialized with {collection.count()} documents")
            return collection
        
        print("Initializing vector database...")
        dataset_path = "data/dataset.txt"
        
        if not os.path.exists(dataset_path):
            print(f"Warning: {dataset_path} not found. Vector DB will be empty.")
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
    except Exception as e:
        print(f"Error initializing vector DB: {e}")
        return None


def retrieve_documents(query, top_k=5):
    """Retrieve the most relevant documents for a query"""
    collection = get_vector_db()
    
    if collection is None or collection.count() == 0:
        return [], []
    
    try:
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
    except Exception as e:
        print(f"Error retrieving documents: {e}")
        return [], []


def get_context_for_query(query, top_k=3):
    """Get formatted context string for a query"""
    documents, scores = retrieve_documents(query, top_k=top_k)
    
    if not documents:
        return "No relevant context found in the database."
    
    context_parts = []
    for i, (doc, score) in enumerate(zip(documents, scores), 1):
        context_parts.append(f"[Document {i} - Relevance: {score:.2f}]\n{doc}\n")
    
    return "\n".join(context_parts)
