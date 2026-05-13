#!/usr/bin/env python3
"""
NexusRAG Comprehensive Benchmark Report Generator
Compares LLM-Only, Basic RAG, and GraphRAG pipelines
"""

import os
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CHROMADB_DISABLE_TELEMETRY"] = "true"

import sys
import time
import json
from datetime import datetime
from tabulate import tabulate
from dotenv import load_dotenv

# Import pipeline functions
from pipelines.logic import run_llm_only, run_basic_rag, run_graph_rag, generate_summary
from pipelines.vector_db import initialize_vector_db
from pipelines.graph_db import initialize_knowledge_graph

load_dotenv()

# Test queries covering different complexity levels
TEST_QUERIES = [
    "What is Valkyria Chronicles III?",
    "When was the Little Rock Arsenal built and why?",
    "What gaming platforms was Valkyria Chronicles III released on?",
    "Who was born at the Little Rock Arsenal and what was their significance?",
    "Describe the gameplay mechanics of Valkyria Chronicles III",
    "What historical events were associated with the Little Rock Arsenal?",
]

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80 + "\n")

def run_benchmark():
    """Run comprehensive benchmarks"""
    print_header("🚀 NexusRAG Comprehensive Benchmark Report")
    print(f"⏰ Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Initialize databases
    print("📦 Initializing systems...")
    try:
        initialize_vector_db()
        print("   ✓ Vector Database initialized")
    except Exception as e:
        print(f"   ⚠ Vector DB initialization: {e}")
    
    try:
        initialize_knowledge_graph()
        print("   ✓ Knowledge Graph initialized")
    except Exception as e:
        print(f"   ⚠ Knowledge Graph initialization: {e}")
    
    # Store results
    results = {
        "llm_only": [],
        "basic_rag": [],
        "graph_rag": [],
        "queries": TEST_QUERIES
    }
    
    # Aggregate metrics
    aggregated = {
        "llm_only": {"latency": [], "cost": [], "tokens_prompt": [], "tokens_completion": [], "bert_score": []},
        "basic_rag": {"latency": [], "cost": [], "tokens_prompt": [], "tokens_completion": [], "bert_score": []},
        "graph_rag": {"latency": [], "cost": [], "tokens_prompt": [], "tokens_completion": [], "bert_score": []}
    }
    
    print_header("🔬 Running Benchmark Queries")
    
    for i, query in enumerate(TEST_QUERIES, 1):
        print(f"\n📍 Query {i}/{len(TEST_QUERIES)}: {query[:60]}...")
        print("-" * 80)
        
        # Run all three pipelines
        print("  Running LLM-Only Pipeline...", end=" ", flush=True)
        res_llm = run_llm_only(query)
        print("✓")
        
        print("  Running Basic RAG Pipeline...", end=" ", flush=True)
        res_rag = run_basic_rag(query)
        print("✓")
        
        print("  Running GraphRAG Pipeline...", end=" ", flush=True)
        res_graph = run_graph_rag(query)
        print("✓")
        
        # Store results
        results["llm_only"].append({
            "query": query,
            "latency_ms": res_llm["latency_ms"],
            "cost": res_llm["cost"],
            "tokens_prompt": res_llm["tokens_prompt"],
            "tokens_completion": res_llm["tokens_completion"],
            "bert_score": res_llm["bert_score"],
            "answer_preview": res_llm["answer"][:100] + "..."
        })
        
        results["basic_rag"].append({
            "query": query,
            "latency_ms": res_rag["latency_ms"],
            "cost": res_rag["cost"],
            "tokens_prompt": res_rag["tokens_prompt"],
            "tokens_completion": res_rag["tokens_completion"],
            "bert_score": res_rag["bert_score"],
            "answer_preview": res_rag["answer"][:100] + "..."
        })
        
        results["graph_rag"].append({
            "query": query,
            "latency_ms": res_graph["latency_ms"],
            "cost": res_graph["cost"],
            "tokens_prompt": res_graph["tokens_prompt"],
            "tokens_completion": res_graph["tokens_completion"],
            "bert_score": res_graph["bert_score"],
            "answer_preview": res_graph["answer"][:100] + "..."
        })
        
        # Aggregate metrics
        aggregated["llm_only"]["latency"].append(res_llm["latency_ms"])
        aggregated["llm_only"]["cost"].append(res_llm["cost"])
        aggregated["llm_only"]["tokens_prompt"].append(res_llm["tokens_prompt"])
        aggregated["llm_only"]["tokens_completion"].append(res_llm["tokens_completion"])
        aggregated["llm_only"]["bert_score"].append(res_llm["bert_score"])
        
        aggregated["basic_rag"]["latency"].append(res_rag["latency_ms"])
        aggregated["basic_rag"]["cost"].append(res_rag["cost"])
        aggregated["basic_rag"]["tokens_prompt"].append(res_rag["tokens_prompt"])
        aggregated["basic_rag"]["tokens_completion"].append(res_rag["tokens_completion"])
        aggregated["basic_rag"]["bert_score"].append(res_rag["bert_score"])
        
        aggregated["graph_rag"]["latency"].append(res_graph["latency_ms"])
        aggregated["graph_rag"]["cost"].append(res_graph["cost"])
        aggregated["graph_rag"]["tokens_prompt"].append(res_graph["tokens_prompt"])
        aggregated["graph_rag"]["tokens_completion"].append(res_graph["tokens_completion"])
        aggregated["graph_rag"]["bert_score"].append(res_graph["bert_score"])
        
        # Print individual query results
        comparison_data = [
            ["Metric", "LLM-Only", "Basic RAG", "GraphRAG"],
            ["Latency (ms)", f"{res_llm['latency_ms']}", f"{res_rag['latency_ms']}", f"{res_graph['latency_ms']}"],
            ["Cost ($)", f"${res_llm['cost']:.4f}", f"${res_rag['cost']:.4f}", f"${res_graph['cost']:.4f}"],
            ["Prompt Tokens", f"{res_llm['tokens_prompt']}", f"{res_rag['tokens_prompt']}", f"{res_graph['tokens_prompt']}"],
            ["Completion Tokens", f"{res_llm['tokens_completion']}", f"{res_rag['tokens_completion']}", f"{res_graph['tokens_completion']}"],
            ["BERT Score", f"{res_llm['bert_score']:.2f}", f"{res_rag['bert_score']:.2f}", f"{res_graph['bert_score']:.2f}"],
        ]
        print("\n" + tabulate(comparison_data, headers="firstrow", tablefmt="grid"))
    
    # Generate Summary Statistics
    print_header("📊 Aggregated Benchmark Results")
    
    summary_data = []
    for pipeline in ["llm_only", "basic_rag", "graph_rag"]:
        agg = aggregated[pipeline]
        if agg["latency"]:
            summary_data.append([
                pipeline.replace("_", " ").title(),
                f"{sum(agg['latency']) / len(agg['latency']):.0f}",
                f"{sum(agg['cost']) / len(agg['cost']) if agg['cost'] else 0:.4f}",
                f"{sum(agg['tokens_prompt']) / len(agg['tokens_prompt']) if agg['tokens_prompt'] else 0:.0f}",
                f"{sum(agg['tokens_completion']) / len(agg['tokens_completion']) if agg['tokens_completion'] else 0:.0f}",
                f"{sum(agg['bert_score']) / len(agg['bert_score']):.2f}",
            ])
    
    summary_headers = ["Pipeline", "Avg Latency (ms)", "Avg Cost ($)", "Avg Prompt Tokens", "Avg Completion Tokens", "Avg BERT Score"]
    print(tabulate(summary_data, headers=summary_headers, tablefmt="grid"))
    
    # Performance Analysis
    print_header("🎯 Performance Analysis")
    
    avg_latency_llm = sum(aggregated["llm_only"]["latency"]) / len(aggregated["llm_only"]["latency"])
    avg_latency_rag = sum(aggregated["basic_rag"]["latency"]) / len(aggregated["basic_rag"]["latency"])
    avg_latency_graph = sum(aggregated["graph_rag"]["latency"]) / len(aggregated["graph_rag"]["latency"])
    
    avg_cost_llm = sum(aggregated["llm_only"]["cost"]) / len(aggregated["llm_only"]["cost"])
    avg_cost_rag = sum(aggregated["basic_rag"]["cost"]) / len(aggregated["basic_rag"]["cost"])
    avg_cost_graph = sum(aggregated["graph_rag"]["cost"]) / len(aggregated["graph_rag"]["cost"])
    
    avg_bert_llm = sum(aggregated["llm_only"]["bert_score"]) / len(aggregated["llm_only"]["bert_score"])
    avg_bert_rag = sum(aggregated["basic_rag"]["bert_score"]) / len(aggregated["basic_rag"]["bert_score"])
    avg_bert_graph = sum(aggregated["graph_rag"]["bert_score"]) / len(aggregated["graph_rag"]["bert_score"])
    
    print(f"""
🚄 LATENCY COMPARISON:
   • LLM-Only:    {avg_latency_llm:.0f} ms (Baseline)
   • Basic RAG:   {avg_latency_rag:.0f} ms ({((avg_latency_rag/avg_latency_llm - 1) * 100):+.1f}%)
   • GraphRAG:    {avg_latency_graph:.0f} ms ({((avg_latency_graph/avg_latency_llm - 1) * 100):+.1f}%)

💰 COST COMPARISON:
   • LLM-Only:    ${avg_cost_llm:.4f} (Baseline)
   • Basic RAG:   ${avg_cost_rag:.4f} ({((avg_cost_rag/avg_cost_llm - 1) * 100):+.1f}%)
   • GraphRAG:    ${avg_cost_graph:.4f} ({((avg_cost_graph/avg_cost_llm - 1) * 100):+.1f}%)

🎯 ACCURACY (BERT Score):
   • LLM-Only:    {avg_bert_llm:.2f} (Baseline)
   • Basic RAG:   {avg_bert_rag:.2f} ({((avg_bert_rag/avg_bert_llm - 1) * 100):+.1f}%)
   • GraphRAG:    {avg_bert_graph:.2f} ({((avg_bert_graph/avg_bert_llm - 1) * 100):+.1f}%)
    """)
    
    # Key Findings
    print_header("💡 Key Findings & Recommendations")
    
    if avg_bert_graph > avg_bert_rag > avg_bert_llm:
        print("""
✓ GraphRAG demonstrates the highest accuracy, leveraging knowledge graph relationships
  for more contextually aware responses.

✓ Basic RAG provides a middle ground with semantic search capabilities,
  outperforming baseline LLM but less sophisticated than GraphRAG.

✓ LLM-Only baseline suffers from lack of context and is prone to hallucinations
  on domain-specific queries.

📌 RECOMMENDATION: Use GraphRAG for complex, multi-hop reasoning queries that require
  entity relationships and contextual understanding.
        """)
    
    # Save detailed results to JSON
    report_file = "benchmark_results.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n📁 Detailed results saved to: {report_file}")
    
    print_header("✅ Benchmark Complete")

if __name__ == "__main__":
    run_benchmark()
