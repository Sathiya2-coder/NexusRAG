# NexusRAG Platform

NexusRAG is a high-performance benchmark dashboard built for the GraphRAG Hackathon Government Division. It compares traditional LLM inference, Basic RAG, and GraphRAG architectures side-by-side.

## Features
- **Benchmark Dashboard**: Compares pipelines live using Groq's Llama-3 API.
- **AI Judge Verdict**: Uses an LLM-as-a-judge to evaluate pipeline answers.
- **Data Explorer**: View and download the raw WikiText-2 dataset.
- **Workflow**: Detailed architecture diagrams and explanations.
- **Vector Database**: ChromaDB-backed semantic search for Basic RAG pipeline.
- **Knowledge Graph**: NetworkX-based entity and relationship extraction for GraphRAG pipeline.

## Setup
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run `python download_data.py` to fetch the WikiText-2 dataset.
4. Run `python setup_vector_db.py` to initialize the ChromaDB vector database (required for Basic RAG).
5. Run `python setup_graph_db.py` to build the knowledge graph (required for GraphRAG).
6. Set your `GROQ_API_KEY` in a `.env` file.
7. Run the app: `streamlit run app.py`

## Architecture

### LLM-Only (Baseline)
- Direct query to Llama-3 with no context
- Baseline for comparison

### Basic RAG
- **Vector Database**: ChromaDB with sentence-transformers embedding model (`all-MiniLM-L6-v2`)
- **Chunking**: 500-token chunks with 100-token overlap
- **Retrieval**: Semantic similarity search (top-3 documents)
- **Storage**: Persistent in `data/chroma_db/`

### GraphRAG  
- **Knowledge Graph**: NetworkX-based directed graph
- **Entity Extraction**: Pattern-based extraction from text
- **Relationship Types**: `is_type_of`, `has`, `founded_by`, `related_to`
- **Traversal**: BFS-based multi-hop entity relationship discovery (up to 2 hops)
- **Storage**: Persistent pickle format in `data/knowledge_graph.pkl`

## Usage

### View Vector Database
```bash
python view_vector_db.py
```

### View Knowledge Graph
```bash
python view_graph_db.py
```

### Test Pipelines
```bash
# Test Basic RAG
python test_basicrag_connection.py

# Test GraphRAG (coming soon)
python test_graphrag_connection.py
```

