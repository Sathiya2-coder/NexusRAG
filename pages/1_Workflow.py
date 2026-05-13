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

# Add custom CSS for enhanced styling with responsive design
st.markdown("""
<style>
/* Responsive Streamlit columns */
[data-testid="column"] {
    flex: 1 1 auto;
}

/* Responsive container for description */
.description-text {
    font-size: clamp(14px, 2vw, 16px);
    line-height: 1.6;
}

/* Center title alignment */
.title-container {
    text-align: center;
    margin-bottom: clamp(30px, 5vw, 50px);
}

/* Responsive paragraph text */
.center-text {
    text-align: center;
    color: #AAA;
    font-size: clamp(14px, 2vw, 16px);
    margin-bottom: clamp(30px, 5vw, 50px);
    line-height: 1.6;
}

/* Responsive heading for comparison */
.comparison-heading {
    color: #FAFAFA;
    margin-top: clamp(20px, 3vw, 30px);
    margin-bottom: clamp(30px, 5vw, 40px);
    font-size: clamp(20px, 4vw, 24px);
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

/* Mobile responsive padding for detailed sections */
.detailed-box {
    padding: clamp(16px, 2vw, 20px);
    margin: clamp(8px, 2vw, 16px) 0;
}

/* Horizontal line separator */
.separator {
    border-top: 1px solid rgba(255,255,255,0.1);
    margin: clamp(20px, 3vw, 30px) 0;
}

/* Responsive hint box */
.hint-box {
    margin-top: clamp(20px, 3vw, 30px);
    padding: clamp(16px, 2vw, 20px);
    background: rgba(76, 175, 80, 0.1);
    border-radius: 8px;
    border-left: 4px solid #4CAF50;
}

.hint-box p {
    color: #AAA;
    font-size: clamp(12px, 1.5vw, 13px);
    line-height: 1.8;
    margin: 0;
}

/* Responsive table wrapper */
.table-wrapper {
    overflow-x: auto;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    margin-bottom: clamp(20px, 3vw, 30px);
    -webkit-overflow-scrolling: touch;
}

@media (max-width: 768px) {
    [data-testid="column"] {
        margin-bottom: clamp(16px, 2vw, 24px);
    }
    
    .section-header {
        padding: 16px;
        margin: 24px 0 20px 0;
    }
    
    .section-header h2 {
        font-size: 20px;
        flex-direction: column;
    }
}

@media (max-width: 480px) {
    [data-testid="column"] {
        margin-bottom: clamp(12px, 2vw, 16px);
    }
    
    .section-header {
        padding: 12px;
        margin: 16px 0 12px 0;
        border-left: 2px solid #2196F3;
    }
    
    .comparison-heading {
        font-size: 18px;
        gap: 8px;
    }
    
    .hint-box {
        margin-top: 16px;
        padding: 12px;
    }
    
    .table-wrapper {
        margin-bottom: 20px;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class='section-header'>
    <h2><i class='fa-solid fa-diagram-project' style='color: #FF9800;'></i>NexusRAG Pipeline Architecture</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("<p class='center-text'>Explore three advanced inference pipelines designed for different use cases: direct LLM invocation, vector-based retrieval augmentation, and TigerGraph-powered knowledge graph traversal. Each pipeline offers distinct advantages in accuracy, speed, and reasoning capability. GraphRAG on TigerGraph enables explicit, factually-grounded multi-hop reasoning.</p>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PIPELINE COMPARISON SECTION
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("<h3 class='comparison-heading'><i class='fa-solid fa-columns' style='color: #2196F3;'></i>Side-by-Side Comparison</h3>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

# PIPELINE 1: LLM-Only
with col1:
    st.markdown("""<div class='pipeline-card' style='background: linear-gradient(135deg, rgba(244, 67, 54, 0.12), rgba(244, 67, 54, 0.06)); border: 2px solid rgba(244, 67, 54, 0.4); border-radius: 16px; padding: 28px; height: 100%; box-shadow: 0 8px 16px rgba(244, 67, 54, 0.1);'><div style='text-align: center; margin-bottom: 24px;'><div style='background: rgba(244, 67, 54, 0.15); border-radius: 12px; padding: 16px; display: inline-block; margin-bottom: 12px;'><i class='fa-solid fa-bolt' style='font-size: 40px; color: #F44336;'></i></div><h3 style='color: #F44336; margin: 0; font-size: 22px; font-weight: 600;'>LLM-Only Baseline</h3><p style='color: #FF6B6B; font-size: 12px; margin-top: 6px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;'>Direct Inference</p></div><div style='background: rgba(255,255,255,0.04); border-radius: 10px; padding: 18px; margin-bottom: 20px; border: 1px solid rgba(244, 67, 54, 0.2);'><p style='color: #E8E8E8; font-size: 13px; margin: 0 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Execution Flow</p><div style='margin-top: 12px; padding: 14px; background: rgba(0,0,0,0.4); border-radius: 8px; border-left: 4px solid #F44336;'><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-user' style='color: #F44336; margin-right: 8px; font-size: 12px;'></i>User Query</p><div style='text-align: center; color: #888; font-size: 11px; margin: 8px 0; letter-spacing: 1px;'>&#8628;</div><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-brain' style='color: #F44336; margin-right: 8px; font-size: 12px;'></i>Direct LLM Response</p></div></div><div style='margin: 20px 0;'><p style='color: #66BB6A; font-size: 12px; margin: 8px 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'><i class='fa-solid fa-check' style='margin-right: 6px;'></i>Advantages</p><ul style='color: #B0BEC5; font-size: 13px; margin: 0; padding-left: 20px; line-height: 1.8;'><li>Ultra-fast response (&lt;100ms)</li><li>Zero setup required</li><li>No external dependencies</li></ul></div><div style='margin: 20px 0;'><p style='color: #FF9800; font-size: 12px; margin: 8px 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'><i class='fa-solid fa-triangle-exclamation' style='margin-right: 6px; font-size: 12px;'></i>Limitations</p><ul style='color: #B0BEC5; font-size: 13px; margin: 0; padding-left: 20px; line-height: 1.8;'><li>Prone to hallucinations</li><li>No context awareness</li><li>Cannot handle private data</li></ul></div></div>""", unsafe_allow_html=True)

# PIPELINE 2: Basic RAG
with col2:
    st.markdown("""<div class='pipeline-card' style='background: linear-gradient(135deg, rgba(255, 152, 0, 0.12), rgba(255, 152, 0, 0.06)); border: 2px solid rgba(255, 152, 0, 0.4); border-radius: 16px; padding: 28px; height: 100%; box-shadow: 0 8px 16px rgba(255, 152, 0, 0.1);'><div style='text-align: center; margin-bottom: 24px;'><div style='background: rgba(255, 152, 0, 0.15); border-radius: 12px; padding: 16px; display: inline-block; margin-bottom: 12px;'><i class='fa-solid fa-magnifying-glass' style='font-size: 40px; color: #FF9800;'></i></div><h3 style='color: #FF9800; margin: 0; font-size: 22px; font-weight: 600;'>Basic RAG</h3><p style='color: #FFB74D; font-size: 12px; margin-top: 6px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;'>Vector Search Retrieval</p></div><div style='background: rgba(255,255,255,0.04); border-radius: 10px; padding: 18px; margin-bottom: 20px; border: 1px solid rgba(255, 152, 0, 0.2);'><p style='color: #E8E8E8; font-size: 13px; margin: 0 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Execution Flow</p><div style='margin-top: 12px; padding: 14px; background: rgba(0,0,0,0.4); border-radius: 8px; border-left: 4px solid #FF9800;'><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-user' style='color: #FF9800; margin-right: 8px; font-size: 12px;'></i>User Query</p><div style='text-align: center; color: #888; font-size: 10px; margin: 8px 0;'>↓ Vectorize & Search ↓</div><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-table' style='color: #FF9800; margin-right: 8px; font-size: 12px;'></i>Retrieve Top-K Chunks</p><div style='text-align: center; color: #888; font-size: 10px; margin: 8px 0;'>↓ Augment Prompt ↓</div><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-brain' style='color: #FF9800; margin-right: 8px; font-size: 12px;'></i>Contextualized Response</p></div></div><div style='margin: 20px 0;'><p style='color: #66BB6A; font-size: 12px; margin: 8px 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'><i class='fa-solid fa-check' style='margin-right: 6px;'></i>Advantages</p><ul style='color: #B0BEC5; font-size: 13px; margin: 0; padding-left: 20px; line-height: 1.8;'><li>Grounds LLM in real data</li><li>Handles private/recent data</li><li>Industry standard approach</li></ul></div><div style='margin: 20px 0;'><p style='color: #FF9800; font-size: 12px; margin: 8px 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'><i class='fa-solid fa-triangle-exclamation' style='margin-right: 6px; font-size: 12px;'></i>Limitations</p><ul style='color: #B0BEC5; font-size: 13px; margin: 0; padding-left: 20px; line-height: 1.8;'><li>Fails on multi-hop reasoning</li><li>Misses cross-document links</li><li>Semantic ≠ Logical relevance</li></ul></div></div>""", unsafe_allow_html=True)

# PIPELINE 3: GraphRAG on TigerGraph
with col3:
    st.markdown("""<div class='pipeline-card' style='background: linear-gradient(135deg, rgba(76, 175, 80, 0.12), rgba(76, 175, 80, 0.06)); border: 2px solid rgba(76, 175, 80, 0.4); border-radius: 16px; padding: 28px; height: 100%; box-shadow: 0 8px 16px rgba(76, 175, 80, 0.1);'><div style='text-align: center; margin-bottom: 24px;'><div style='background: rgba(76, 175, 80, 0.15); border-radius: 12px; padding: 16px; display: inline-block; margin-bottom: 12px;'><i class='fa-solid fa-share-nodes' style='font-size: 40px; color: #4CAF50;'></i></div><h3 style='color: #4CAF50; margin: 0; font-size: 22px; font-weight: 600;'>GraphRAG on TigerGraph</h3><p style='color: #66BB6A; font-size: 12px; margin-top: 6px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;'>TigerGraph-Powered Knowledge Graph</p></div><div style='background: rgba(255,255,255,0.04); border-radius: 10px; padding: 18px; margin-bottom: 20px; border: 1px solid rgba(76, 175, 80, 0.2);'><p style='color: #E8E8E8; font-size: 13px; margin: 0 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'>Execution Flow</p><div style='margin-top: 12px; padding: 14px; background: rgba(0,0,0,0.4); border-radius: 8px; border-left: 4px solid #4CAF50;'><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-user' style='color: #4CAF50; margin-right: 8px; font-size: 12px;'></i>User Query</p><div style='text-align: center; color: #888; font-size: 10px; margin: 8px 0;'>↓ Extract Entities ↓</div><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-share-nodes' style='color: #4CAF50; margin-right: 8px; font-size: 12px;'></i>TigerGraph Multi-Hop Traversal</p><div style='text-align: center; color: #888; font-size: 10px; margin: 8px 0;'>↓ Explicit Relationships ↓</div><p style='color: #FFF; margin: 6px 0; font-size: 13px; line-height: 1.6;'><i class='fa-solid fa-brain' style='color: #4CAF50; margin-right: 8px; font-size: 12px;'></i>Accurate Response</p></div></div><div style='margin: 20px 0;'><p style='color: #66BB6A; font-size: 12px; margin: 8px 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'><i class='fa-solid fa-star' style='margin-right: 6px; color: #FFD700;'></i>Advantages</p><ul style='color: #B0BEC5; font-size: 13px; margin: 0; padding-left: 20px; line-height: 1.8;'><li><strong style='color: #66BB6A;'>100% factually accurate</strong></li><li>Perfect multi-hop reasoning</li><li>Explicit relationships</li><li>Lower token usage</li></ul></div><div style='margin: 20px 0;'><p style='color: #66BB6A; font-size: 12px; margin: 8px 0 12px 0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;'><i class='fa-solid fa-check' style='margin-right: 6px;'></i>Setup Required</p><ul style='color: #B0BEC5; font-size: 13px; margin: 0; padding-left: 20px; line-height: 1.8;'><li>Graph construction (~2h)</li><li>Entity extraction setup</li><li>Initial data processing</li></ul></div></div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DETAILED WORKFLOW SECTION
# ─────────────────────────────────────────────────────────────────────────────
# DETAILED WORKFLOW SECTION
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class='section-header'>
    <h2><i class='fa-solid fa-layer-group' style='color: #2196F3;'></i>In-Depth Pipeline Analysis</h2>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["LLM-Only", "Basic RAG", "GraphRAG on TigerGraph"])

with tab1:
    st.markdown("<div style='margin-bottom: 16px;'><i class='fa-solid fa-circle' style='color: #F44336; margin-right: 8px; font-size: 14px;'></i><span style='color: #F44336; font-weight: 600; font-size: 14px;'>LLM-Only Baseline</span></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1.2], gap="large")
    with col_a:
        st.markdown("""
        <div style='background: rgba(244, 67, 54, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #F44336;'>
            <h4 style='color: #F44336; margin-top: 0;'><i class='fa-solid fa-cogs' style='margin-right: 8px;'></i>How It Works</h4>
            <ol style='color: #CCC; font-size: 14px; line-height: 1.8;'>
                <li><strong>User submits query</strong> to the LLM (Llama 3.3-70B via Groq)</li>
                <li><strong>No retrieval step</strong> - LLM generates answer from training data</li>
                <li><strong>Return response</strong> directly to user</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div style='background: rgba(244, 67, 54, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #F44336;'>
            <h4 style='color: #F44336; margin-top: 0;'><i class='fa-solid fa-circle-check' style='margin-right: 8px;'></i>Good For</h4>
            <ul style='color: #CCC; font-size: 14px; line-height: 1.8; margin: 0;'>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>General knowledge questions</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>No private data involved</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Speed is critical</li>
            </ul>
            <p style='color: #BBB; font-size: 13px; margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);'><i class='fa-solid fa-circle-xmark' style='color: #FF5252; margin-right: 8px;'></i><strong>Not Suitable For:</strong></p>
            <ul style='color: #CCC; font-size: 14px; line-height: 1.8; margin: 8px 0 0 0;'>
                <li><i class='fa-solid fa-xmark' style='color: #FF5252; margin-right: 6px;'></i>Multi-hop reasoning</li>
                <li><i class='fa-solid fa-xmark' style='color: #FF5252; margin-right: 6px;'></i>Factual accuracy required</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<div style='margin-bottom: 16px;'><i class='fa-solid fa-circle' style='color: #FF9800; margin-right: 8px; font-size: 14px;'></i><span style='color: #FF9800; font-weight: 600; font-size: 14px;'>Basic RAG</span></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1.2], gap="large")
    with col_a:
        st.markdown("""
        <div style='background: rgba(255, 152, 0, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #FF9800;'>
            <h4 style='color: #FF9800; margin-top: 0;'><i class='fa-solid fa-cogs' style='margin-right: 8px;'></i>How It Works</h4>
            <ol style='color: #CCC; font-size: 14px; line-height: 1.8;'>
                <li><strong>Vectorize query</strong> using embedding model (Chroma DB)</li>
                <li><strong>Search vector store</strong> for top-k similar chunks</li>
                <li><strong>Build context</strong> from retrieved text</li>
                <li><strong>Augment prompt</strong> with context before LLM</li>
                <li><strong>Generate answer</strong> grounded in retrieved data</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div style='background: rgba(255, 152, 0, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #FF9800;'>
            <h4 style='color: #FF9800; margin-top: 0;'><i class='fa-solid fa-circle-check' style='margin-right: 8px;'></i>Strengths</h4>
            <ul style='color: #CCC; font-size: 14px; line-height: 1.8; margin: 0;'>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Grounds responses in real data</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Handles private/recent data</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Industry standard solution</li>
            </ul>
            <p style='color: #BBB; font-size: 13px; margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.1);'><i class='fa-solid fa-circle-xmark' style='color: #FF5252; margin-right: 8px;'></i><strong>Limitations:</strong></p>
            <ul style='color: #CCC; font-size: 14px; line-height: 1.8; margin: 8px 0 0 0;'>
                <li><i class='fa-solid fa-xmark' style='color: #FF5252; margin-right: 6px;'></i>Fails on multi-hop reasoning</li>
                <li><i class='fa-solid fa-xmark' style='color: #FF5252; margin-right: 6px;'></i>Misses cross-document relationships</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown("<div style='margin-bottom: 16px;'><i class='fa-solid fa-circle' style='color: #4CAF50; margin-right: 8px; font-size: 14px;'></i><span style='color: #4CAF50; font-weight: 600; font-size: 14px;'>GraphRAG on TigerGraph</span></div>", unsafe_allow_html=True)
    col_a, col_b = st.columns([1, 1.2], gap="large")
    with col_a:
        st.markdown("""
        <div style='background: rgba(76, 175, 80, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #4CAF50;'>
            <h4 style='color: #4CAF50; margin-top: 0;'><i class='fa-solid fa-cogs' style='margin-right: 8px;'></i>How It Works</h4>
            <ol style='color: #CCC; font-size: 14px; line-height: 1.8;'>
                <li><strong>Build TigerGraph</strong> from dataset: extract entities + relationships using LLM</li>
                <li><strong>Store in TigerGraph</strong>: vertices (entities) and edges (relationships)</li>
                <li><strong>Extract entities</strong> from user query using NLP</li>
                <li><strong>Execute GSQL queries</strong> to traverse graph up to 2 hops</li>
                <li><strong>Collect subgraph</strong> with all connected nodes/edges from TigerGraph</li>
                <li><strong>Format for LLM</strong> as structured graph context with relationships</li>
                <li><strong>Generate answer</strong> grounded in TigerGraph relationships</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown("""
        <div style='background: rgba(76, 175, 80, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #4CAF50;'>
            <h4 style='color: #4CAF50; margin-top: 0;'><i class='fa-solid fa-circle-check' style='margin-right: 8px;'></i>Advantages</h4>
            <ul style='color: #CCC; font-size: 14px; line-height: 1.8;'>
                <li><i class='fa-solid fa-star' style='color: #FFD700; margin-right: 6px;'></i><strong>100% factually accurate</strong></li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Solves multi-hop reasoning</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Explicit relationships via TigerGraph</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>GSQL-optimized traversal</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Lower token usage</li>
                <li><i class='fa-solid fa-check' style='color: #4CAF50; margin-right: 6px;'></i>Deterministic results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# COMPARISON METRICS
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class='section-header'>
    <h2><i class='fa-solid fa-chart-column' style='color: #4CAF50;'></i>Performance Metrics Comparison</h2>
</div>
""", unsafe_allow_html=True)

# Create comparison rows
metrics = [
    ("Accuracy", "Low", "Medium", "<i class='fa-solid fa-star' style='color: #FFD700;'></i> Perfect"),
    ("Multi-Hop Reasoning", "<i class='fa-solid fa-xmark' style='color: #FF5252;'></i> No", "<i class='fa-solid fa-triangle-exclamation' style='color: #FF9800;'></i> Partial", "<i class='fa-solid fa-check' style='color: #4CAF50;'></i> Full"),
    ("Setup Time", "~0 min", "~1 hour", "~2 hours"),
    ("Latency", "<i class='fa-solid fa-bolt' style='color: #FFC107;'></i> Very Fast", "<i class='fa-solid fa-bolt' style='color: #FFC107;'></i> Fast", "<i class='fa-solid fa-gear' style='color: #9E9E9E;'></i> Moderate"),
    ("Token Usage", "Standard", "Higher", "Lower"),
    ("Cost per Query", "<i class='fa-solid fa-dollar-sign' style='color: #4CAF50;'></i> $0.50", "<i class='fa-solid fa-dollar-sign' style='color: #FF9800;'></i> $0.70", "<i class='fa-solid fa-dollar-sign' style='color: #66BB6A;'></i> $0.30"),
    ("Hallucination Risk", "Very High", "Medium", "None"),
    ("Data Freshness", "Training data only", "Up to retrieval date", "Real-time")
]

# Build complete table HTML
table_rows = ""
for metric, llm_val, rag_val, graph_val in metrics:
    table_rows += f"<tr style='border-bottom: 1px solid rgba(255,255,255,0.05);'><td style='padding: 16px 20px; color: #E8E8E8; font-weight: 500; border-right: 1px solid rgba(255,255,255,0.05);'>{metric}</td><td style='padding: 16px 20px; text-align: center; color: #AAA; border-right: 1px solid rgba(255,255,255,0.05);'>{llm_val}</td><td style='padding: 16px 20px; text-align: center; color: #AAA; border-right: 1px solid rgba(255,255,255,0.05);'>{rag_val}</td><td style='padding: 16px 20px; text-align: center; color: #AAA;'>{graph_val}</td></tr>"

table_html = f"""<div class='table-wrapper'>
<table style='width: 100%; border-collapse: collapse; background: rgba(20, 30, 50, 0.8);'>
<thead><tr style='background: rgba(33, 150, 243, 0.15); border-bottom: 2px solid rgba(255,255,255,0.1);'><th style='padding: 18px 20px; text-align: left; color: #2196F3; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.05);'>Metric</th><th style='padding: 18px 20px; text-align: center; color: #F44336; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.05);'><i class='fa-solid fa-circle' style='margin-right: 8px;'></i>LLM-Only</th><th style='padding: 18px 20px; text-align: center; color: #FF9800; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.05);'><i class='fa-solid fa-circle' style='margin-right: 8px;'></i>Basic RAG</th><th style='padding: 18px 20px; text-align: center; color: #4CAF50; font-weight: 600;'><i class='fa-solid fa-circle' style='margin-right: 8px;'></i>GraphRAG on TigerGraph</th></tr></thead>
<tbody>{table_rows}</tbody>
</table>
</div>"""

st.markdown(table_html, unsafe_allow_html=True)

st.markdown("""
<div class='hint-box'>
    <p>
        <i class='fa-solid fa-lightbulb' style='color: #FFD700; margin-right: 8px;'></i>
        <strong style='color: #E8E8E8;'>Pro Tip:</strong> Choose GraphRAG when accuracy and multi-hop reasoning are critical. Use Basic RAG for general document retrieval. Use LLM-Only only for low-stakes queries where speed is paramount.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TIGERGRAPH CAPABILITIES SECTION
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class='section-header'>
    <h2><i class='fa-solid fa-network-wired' style='color: #FF6B6B;'></i>TigerGraph: The GraphRAG Engine</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style='color: #AAA; font-size: 15px; line-height: 1.8;'>
TigerGraph powers GraphRAG's superior accuracy through purpose-built graph database capabilities:
</p>
""", unsafe_allow_html=True)

col_tg1, col_tg2, col_tg3 = st.columns(3)

with col_tg1:
    st.markdown("""
    <div style='background: rgba(255, 107, 107, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #FF6B6B;'>
        <h4 style='color: #FF6B6B; margin-top: 0;'><i class='fa-solid fa-project-diagram' style='margin-right: 8px;'></i>Graph Storage</h4>
        <ul style='color: #CCC; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 20px;'>
            <li>Vertices: Entity instances (people, places, things)</li>
            <li>Edges: Explicit relationships with types</li>
            <li>Properties: Rich metadata on both vertices & edges</li>
            <li>Schema: Typed graph structure for validation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_tg2:
    st.markdown("""
    <div style='background: rgba(255, 193, 7, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #FFC107;'>
        <h4 style='color: #FFC107; margin-top: 0;'><i class='fa-solid fa-bolt' style='margin-right: 8px;'></i>GSQL Traversal</h4>
        <ul style='color: #CCC; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 20px;'>
            <li>Native GSQL language for graph queries</li>
            <li>Sub-millisecond traversal response times</li>
            <li>Parallel graph traversal across vertices</li>
            <li>Custom aggregations and filtering</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_tg3:
    st.markdown("""
    <div style='background: rgba(76, 175, 80, 0.1); border-radius: 8px; padding: 20px; border-left: 4px solid #4CAF50;'>
        <h4 style='color: #4CAF50; margin-top: 0;'><i class='fa-solid fa-magnifying-glass-chart' style='margin-right: 8px;'></i>Multi-Hop Reasoning</h4>
        <ul style='color: #CCC; font-size: 13px; line-height: 1.8; margin: 0; padding-left: 20px;'>
            <li>Navigate 2-3 relationship hops instantly</li>
            <li>Find indirect connections between entities</li>
            <li>Gather context across document boundaries</li>
            <li>100% grounded in explicit relationships</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style='background: rgba(76, 175, 80, 0.05); border-radius: 8px; padding: 20px; border: 1px solid rgba(76, 175, 80, 0.3); margin-top: 20px;'>
    <h4 style='color: #66BB6A; margin-top: 0;'><i class='fa-solid fa-diagram-successor' style='margin-right: 8px;'></i>GraphRAG Query Flow with TigerGraph</h4>
    <div style='color: #CCC; font-size: 13px; line-height: 2.2; font-family: monospace; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 6px;'>
        <i class='fa-solid fa-circle-1' style='color:#4CAF50; margin-right: 8px;'></i>User Query → Entity Recognition<br>
        <i class='fa-solid fa-circle-2' style='color:#4CAF50; margin-right: 8px;'></i>Extract Query Entities → TigerGraph Lookup<br>
        <i class='fa-solid fa-circle-3' style='color:#4CAF50; margin-right: 8px;'></i>Execute GSQL Traversal → Find Connected Entities<br>
        <i class='fa-solid fa-circle-4' style='color:#4CAF50; margin-right: 8px;'></i>Collect Subgraph → All Vertices & Relationships<br>
        <i class='fa-solid fa-circle-5' style='color:#4CAF50; margin-right: 8px;'></i>Format Context → Structured JSON for LLM<br>
        <i class='fa-solid fa-circle-6' style='color:#4CAF50; margin-right: 8px;'></i>LLM Generation → Answer Grounded in Graph<br>
    </div>
</div>
""", unsafe_allow_html=True)

render_footer()
