import streamlit as st
import os
import pandas as pd
from components import render_header, render_footer

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="NexusRAG Dataset", layout="wide", initial_sidebar_state="collapsed")

with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()

# ── Dataset Explorer ────────────────────────────────────────────────────────
st.markdown("<h2 style='color:#FAFAFA;margin-top:20px;'>WikiText-2 Dataset Explorer</h2>", unsafe_allow_html=True)
st.markdown("""
Explore the raw dataset powering the NexusRAG benchmark. This dataset contains high-quality Wikipedia articles used for training and evaluating large language models.

**How it powers GraphRAG with TigerGraph:**
- **Entity Extraction**: Raw text is processed to identify key entities (people, organizations, events, locations)
- **Relationship Mapping**: LLM-powered extraction identifies explicit relationships between entities
- **TigerGraph Storage**: Entities become vertices and relationships become edges in the knowledge graph
- **Multi-Hop Traversal**: Complex queries leverage TigerGraph's GSQL engine to traverse multiple relationship hops
""")

data_path = "data/dataset.txt"

if not os.path.exists(data_path):
    st.warning("Dataset not found. Please run `python download_data.py` first.")
else:
    file_size_mb = os.path.getsize(data_path) / (1024 * 1024)
    
    # Read the first 1000 lines for preview
    preview_lines = []
    line_count = 0
    with open(data_path, "r", encoding="utf-8") as f:
        for line in f:
            line_count += 1
            if len(preview_lines) < 1000:
                preview_lines.append(line.strip())
    
    # Create an ordered structured DataFrame for the preview
    df_preview = pd.DataFrame({
        "Line #": range(1, len(preview_lines) + 1),
        "Text Content": preview_lines
    })
    # Filter out completely empty lines for a cleaner view
    df_preview = df_preview[df_preview["Text Content"] != ""]

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Size", f"{file_size_mb:.2f} MB")
    with col2:
        st.metric("Total Lines", f"{line_count:,}")
    with col3:
        st.metric("Tokens (approx)", "2,400,000+")

    st.markdown("---")

    # Layout: Preview on left, Download on right
    c_left, c_right = st.columns([3, 1])

    with c_left:
        st.subheader("Data Preview (Structured)")
        st.dataframe(
            df_preview,
            use_container_width=True,
            hide_index=True,
            height=400
        )

    with c_right:
        st.subheader("Download & Graph Use")
        st.markdown("""
Get the full raw text file for local benchmarking and TigerGraph construction.

**Use with TigerGraph:**
1. Download the dataset
2. Run entity/relationship extraction
3. Bulk ingest into TigerGraph
4. Execute GSQL queries for graph traversal
5. Feed results to LLM for accurate answers
        """)
        
        st.markdown('<div class="fa-marker-download"></div>', unsafe_allow_html=True)
        with open(data_path, "rb") as f:
            st.download_button(
                label="Download Full Dataset (.txt)",
                data=f,
                file_name="wikitext_2_raw.txt",
                mime="text/plain",
                type="primary",
                use_container_width=True
            )

render_footer()
