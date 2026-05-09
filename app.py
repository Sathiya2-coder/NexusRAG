import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
from pipelines.logic import run_llm_only, run_basic_rag, run_graph_rag, generate_summary
from components import render_header, render_footer

# Load API keys
load_dotenv(override=True)

@st.cache_resource
def get_groq_client():
    return Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="NexusRAG Dashboard", layout="wide", initial_sidebar_state="collapsed")

with open("style.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

render_header()

# ── Platform Overview ─────────────────────────────────────────────────────────
st.markdown("<h2 style='color:#FAFAFA;margin-top:20px; text-align: center; font-size: 36px; margin-bottom: 5px;'>Welcome to NexusRAG Platform</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888; font-size: 18px; margin-bottom: 40px;'>The next generation of AI inference powered by Knowledge Graphs.</p>", unsafe_allow_html=True)

o_col1, o_col2, o_col3 = st.columns(3)

with o_col1:
    st.markdown("""
    <div class="overview-card">
        <div class="icon-container" style="background: rgba(33, 150, 243, 0.1); color: #2196F3;">
            <i class="fa-solid fa-database fa-2x"></i>
        </div>
        <h3>1. Data Ingestion</h3>
        <p>We process raw unstructured text (WikiText-2) and structure it into a dense format ready for extraction.</p>
    </div>
    """, unsafe_allow_html=True)

with o_col2:
    st.markdown("""
    <div class="overview-card">
        <div class="icon-container" style="background: rgba(255, 152, 0, 0.1); color: #FF9800;">
            <i class="fa-solid fa-project-diagram fa-2x"></i>
        </div>
        <h3>2. Graph Construction</h3>
        <p>Using TigerGraph, entities and relationships are explicitly mapped into a highly connected Knowledge Graph.</p>
    </div>
    """, unsafe_allow_html=True)

with o_col3:
    st.markdown("""
    <div class="overview-card">
        <div class="icon-container" style="background: rgba(76, 175, 80, 0.1); color: #4CAF50;">
            <i class="fa-solid fa-brain fa-2x"></i>
        </div>
        <h3>3. AI Inference</h3>
        <p>Groq's Llama 3 models traverse the graph to answer complex, multi-hop queries with 100% factual accuracy.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border-color:#333; margin: 40px 0;'>", unsafe_allow_html=True)

# ── Benchmark Dashboard ────────────────────────────────────────────────────────
st.markdown("<h2 style='color:#FAFAFA;margin-top:20px;'>1. Benchmark Dashboard</h2>", unsafe_allow_html=True)
st.markdown("Compare **LLM-Only**, **Basic RAG**, and **GraphRAG** side-by-side.")

query = st.text_area("Enter your query:", height=100,
    placeholder="e.g. How do the entities connected to Project X relate to the recent financial outcomes?")

if st.button("Run Benchmark", type="primary"):
    if not query.strip():
        st.warning("Please enter a query to run the benchmark.")
    else:
        with st.spinner("Running pipelines..."):
            res_llm   = run_llm_only(query)
            res_rag   = run_basic_rag(query)
            res_graph = run_graph_rag(query)

        col1, col2, col3 = st.columns(3)

        def render_pipeline(col, title, res, color):
            with col:
                st.subheader(title)
                ah = '<div class="answer-box" style="border-left-color:%%C%%;"><i>"%%A%%"</i></div>'
                ah = ah.replace("%%C%%", color).replace("%%A%%", str(res["answer"]))
                st.markdown(ah, unsafe_allow_html=True)

                total   = res["tokens_prompt"] + res["tokens_completion"]
                badge   = "pass-badge" if res["accuracy_pass"] else "fail-badge"
                label   = "PASS"       if res["accuracy_pass"] else "FAIL"

                mh = (
                    '<div class="metric-card">'
                    '<div class="metric-title"><i class="fa-solid fa-gauge-high"></i> Performance</div>'
                    '<div><b>Latency:</b> %%L%% ms</div>'
                    '<div><b>Cost:</b> $%%CO%%</div>'
                    '<hr style="margin:10px 0;border-color:#444;">'
                    '<div class="metric-title"><i class="fa-solid fa-coins"></i> Tokens</div>'
                    '<div><b>Prompt:</b> %%P%%</div>'
                    '<div><b>Completion:</b> %%CP%%</div>'
                    '<div><b>Total:</b> %%T%%</div>'
                    '<hr style="margin:10px 0;border-color:#444;">'
                    '<div class="metric-title"><i class="fa-solid fa-bullseye"></i> Accuracy</div>'
                    '<div><b>LLM-as-a-Judge:</b> <span class="%%B%%">%%LB%%</span></div>'
                    '<div><b>BERTScore:</b> %%BS%%</div>'
                    '</div>'
                )
                mh = mh.replace("%%L%%",  str(res["latency_ms"]))
                mh = mh.replace("%%CO%%", "{:.5f}".format(res["cost"]))
                mh = mh.replace("%%P%%",  str(res["tokens_prompt"]))
                mh = mh.replace("%%CP%%", str(res["tokens_completion"]))
                mh = mh.replace("%%T%%",  str(total))
                mh = mh.replace("%%B%%",  badge)
                mh = mh.replace("%%LB%%", label)
                mh = mh.replace("%%BS%%", "{:.2f}".format(res["bert_score"]))
                st.markdown(mh, unsafe_allow_html=True)

        render_pipeline(col1, "1. LLM-Only Baseline", res_llm,   "#757575")
        render_pipeline(col2, "2. Basic RAG",          res_rag,   "#FF9800")
        render_pipeline(col3, "3. GraphRAG",            res_graph, "#4CAF50")

        st.markdown("---")
        st.markdown(
            "<h3 style='color:#4CAF50;margin-top:0;'>"
            "<i class='fa-solid fa-robot' style='margin-right:10px;'></i>"
            "Official AI Benchmark Verdict</h3>",
            unsafe_allow_html=True)
        with st.spinner("Generating verdict..."):
            st.info(generate_summary(query, res_llm, res_rag, res_graph))

# ── Floating Chatbot (Native Streamlit) ───────────────────────────────────────
st.markdown("<!-- Chatbot Start -->", unsafe_allow_html=True)

with st.popover("💬", help="Chat with the Dataset"):
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chatbot Header
    st.markdown("""
        <div style='text-align: center; margin-bottom: 16px;'>
            <i class='fa-solid fa-robot' style='color:#FF9800; font-size: 32px; margin-bottom: 8px;'></i>
            <h3 style='margin:0; color:#FAFAFA;'>Dataset Assistant</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Suggested question chips (only before first message)
    if not st.session_state.messages and "trigger_chat" not in st.session_state:
        st.markdown("<p style='color:#888;font-size:14px;margin-bottom:8px;'>Try asking one of these:</p>", unsafe_allow_html=True)
        
        st.markdown('<div class="fa-marker-q1"></div>', unsafe_allow_html=True)
        if st.button("What are the main entities?", key="q1", use_container_width=True):
            st.session_state.trigger_chat = "What are the main entities in this dataset?"
            st.rerun()
            
        st.markdown('<div class="fa-marker-q2"></div>', unsafe_allow_html=True)
        if st.button("How does the graph improve accuracy?", key="q2", use_container_width=True):
            st.session_state.trigger_chat = "How does the graph improve accuracy?"
            st.rerun()
            
        st.markdown('<div class="fa-marker-q3"></div>', unsafe_allow_html=True)
        if st.button("Find connections between entities.", key="q3", use_container_width=True):
            st.session_state.trigger_chat = "Find connections between entities."
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        # Show clear button only if there are messages
        st.markdown('<div class="fa-marker-clear"></div>', unsafe_allow_html=True)
        if st.button("Clear Chat History", key="clear_chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        st.markdown("<hr style='border-color:#333;margin:10px 0;'>", unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    user_input = st.chat_input("Ask anything about the dataset...")

    # Handle button trigger
    if "trigger_chat" in st.session_state:
        user_input = st.session_state.trigger_chat
        del st.session_state.trigger_chat

    # Process input
    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("_Thinking..._")
            try:
                history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
                completion = get_groq_client().chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": (
                            "You are a concise, expert AI assistant for the NexusRAG Benchmark Dashboard. "
                            "The dataset is WikiText-2 with 2.4 million tokens of high-quality Wikipedia articles "
                            "covering history, science, geography, and notable people. "
                            "Answer in 2-4 sentences max unless more detail is explicitly requested."
                        )}
                    ] + history,
                    temperature=0.7,
                    max_tokens=512,
                )
                full_response = completion.choices[0].message.content
            except Exception as e:
                full_response = f"⚠️ Error: {str(e)}"
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.rerun()

# ── Footer ─────────────────────────────────────────────────────────────────────
render_footer()
