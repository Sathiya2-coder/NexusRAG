import streamlit as st
import os
import sys

# Ensure components can be imported from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from components import render_header, render_footer

st.set_page_config(page_title="NexusRAG Workflow", layout="wide")

# Load external CSS
with open("style.css", "r") as f:
    css = f.read()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

render_header()

st.markdown("<h2 style='color: #FAFAFA; margin-top: 20px; font-family: Arial, sans-serif;'><i class='fa-solid fa-diagram-project' style='margin-right: 10px; color: #FF9800;'></i> NexusRAG Architecture Workflow</h2>", unsafe_allow_html=True)

st.markdown("""
This page details the official architecture and data flow for the NexusRAG inference pipeline compared to traditional baselines.

---

### Pipeline 1: LLM-Only Baseline
In this pipeline, the user's query is sent directly to the Large Language Model (e.g., Llama 3 or Mixtral via Groq).
* **Pros:** Extremely fast, zero setup required.
* **Cons:** Highly prone to hallucinations, cannot answer questions about private or recent data.

### Pipeline 2: Basic RAG (Vector Search)
This is the industry standard today. Documents are chunked and converted into vector embeddings. 
1. The user's query is converted into a vector.
2. The system searches for the top-k most mathematically similar text chunks.
3. These chunks are stuffed into the LLM's prompt context.
* **Pros:** Grounds the LLM in real data.
* **Cons:** Fails at "multi-hop" reasoning. If an answer requires connecting an event in Document A to a person in Document B, vector search often misses the connection.

### Pipeline 3: TigerGraph GraphRAG
This pipeline uses a Knowledge Graph to explicitly map entities (people, places, organizations) and their relationships.
1. The dataset is ingested into TigerGraph, extracting entities and edges.
2. The user's query triggers a multi-hop graph traversal, pulling only the exact sub-graph needed.
3. The LLM receives a highly structured, mathematically precise context prompt.
* **Pros:** Perfect accuracy for complex reasoning, dramatically reduces token usage.
* **Cons:** Requires upfront graph schema design and ingestion.
""")

render_footer()
