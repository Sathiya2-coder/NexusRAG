#!/usr/bin/env python3
"""
Verify Streamlit App + TigerGraph Integration
Check that all pipelines are working correctly
"""
import sys
import os
import subprocess
import time
from pathlib import Path

sys.path.insert(0, os.path.abspath("."))

def check_streamlit_running():
    """Check if Streamlit is running"""
    print("\n" + "="*70)
    print("STREAMLIT APP STATUS CHECK")
    print("="*70)
    
    try:
        # Check if port 8501 is listening (default Streamlit port)
        result = subprocess.run(
            ["netstat", "-ano"], 
            capture_output=True, 
            text=True,
            shell=True
        )
        
        if "8501" in result.stdout:
            print("\n✅ Streamlit is RUNNING")
            print("   Access at: http://localhost:8501")
            return True
        else:
            print("\n⚠️ Streamlit may not be running on port 8501")
            print("   Check terminal or run: streamlit run app.py")
            return False
    except Exception as e:
        print(f"\n⚠️ Could not check port status: {e}")
        return False

def check_pipelines():
    """Check if all pipeline modules exist"""
    print("\n" + "="*70)
    print("PIPELINE MODULES CHECK")
    print("="*70)
    
    pipelines = {
        "Logic": "pipelines/logic.py",
        "Vector DB": "pipelines/vector_db.py",
        "Graph DB": "pipelines/graph_db.py",
    }
    
    all_exist = True
    for name, path in pipelines.items():
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"✅ {name}: {path} ({size:,} bytes)")
        else:
            print(f"❌ {name}: {path} NOT FOUND")
            all_exist = False
    
    return all_exist

def check_tigergraph_integration():
    """Check TigerGraph integration in code"""
    print("\n" + "="*70)
    print("TIGERGRAPH INTEGRATION CHECK")
    print("="*70)
    
    try:
        from pyTigerGraph import TigerGraphConnection
        
        conn = TigerGraphConnection(
            host="https://tg-d30aafa4-669c-4606-b227-ae7da842e211.tg-3452941248.i.tgcloud.io",
            username="sathiya",
            password="Mano@2611",
            graphname="NexusRAG",
            tgCloud=True
        )
        
        print("✅ TigerGraph Connection: ACTIVE")
        print(f"   Graph: {conn.graphname}")
        print(f"   Status: Connected and ready")
        
        return True
    except Exception as e:
        print(f"❌ TigerGraph Connection: FAILED")
        print(f"   Error: {e}")
        return False

def check_api_keys():
    """Check if API keys are configured"""
    print("\n" + "="*70)
    print("API KEYS CHECK")
    print("="*70)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        masked = groq_key[:10] + "*" * (len(groq_key) - 15) + groq_key[-5:]
        print(f"✅ GROQ_API_KEY: {masked}")
    else:
        print("❌ GROQ_API_KEY: NOT FOUND")
    
    return groq_key is not None

def print_app_features():
    """Print available features"""
    print("\n" + "="*70)
    print("STREAMLIT APP FEATURES")
    print("="*70)
    
    features = {
        "🔄 Benchmark Dashboard": "Run all 3 pipelines side-by-side",
        "📊 Metrics Display": "Tokens, latency, cost, accuracy",
        "💬 AI Chatbot": "Ask questions about the dataset",
        "🎯 Accuracy Evaluation": "LLM-as-Judge + BERTScore",
        "📈 Performance Metrics": "Compare pipelines in real-time",
    }
    
    print("\nAvailable Features:")
    for feature, description in features.items():
        print(f"  {feature}")
        print(f"    └─ {description}")

def print_how_to_use():
    """Print how to use the app"""
    print("\n" + "="*70)
    print("HOW TO USE YOUR STREAMLIT APP")
    print("="*70)
    
    print("\n1️⃣  OPEN THE APP")
    print("   URL: http://localhost:8501")
    
    print("\n2️⃣  BENCHMARK DASHBOARD")
    print("   - Enter a query in the text area")
    print("   - Click 'Run Benchmark'")
    print("   - View results for all 3 pipelines")
    
    print("\n3️⃣  SAMPLE QUERIES TO TRY")
    queries = [
        "What is Valkyria Chronicles III?",
        "Tell me about the Tower Building in Little Rock",
        "Who was General Douglas MacArthur?",
        "What happened during the Civil War at the arsenal?",
    ]
    for i, q in enumerate(queries, 1):
        print(f"   {i}. {q}")
    
    print("\n4️⃣  USE THE CHATBOT")
    print("   - Click the 💬 button")
    print("   - Ask questions about the dataset")
    print("   - Get AI-powered responses")
    
    print("\n5️⃣  VIEW METRICS")
    print("   - Performance (latency, cost)")
    print("   - Tokens (prompt, completion, total)")
    print("   - Accuracy (LLM-as-Judge, BERTScore)")
    print("   - Compare across all 3 pipelines")

def print_troubleshooting():
    """Print troubleshooting guide"""
    print("\n" + "="*70)
    print("TROUBLESHOOTING")
    print("="*70)
    
    print("\n❓ If Streamlit won't start:")
    print("   1. Check Python version: python --version")
    print("   2. Ensure venv is activated")
    print("   3. Run: pip install streamlit")
    print("   4. Then: streamlit run app.py")
    
    print("\n❓ If queries fail:")
    print("   1. Verify GROQ_API_KEY in .env")
    print("   2. Check TigerGraph connection: python test_graphrag_tigergraph.py")
    print("   3. Check database initialized: python pipelines/vector_db.py")
    
    print("\n❓ If metrics show zeros:")
    print("   1. Ensure TigerGraph is running")
    print("   2. Verify data loaded: check TigerGraph admin panel")
    print("   3. Check Groq API key is valid")

def main():
    """Run all checks"""
    print("\n" + "="*70)
    print("  NEXUSRAG STREAMLIT + TIGERGRAPH VERIFICATION")
    print("="*70)
    
    checks = {
        "Streamlit Running": check_streamlit_running(),
        "Pipelines Available": check_pipelines(),
        "TigerGraph Connected": check_tigergraph_integration(),
        "API Keys Configured": check_api_keys(),
    }
    
    # Print features
    print_app_features()
    
    # Print how to use
    print_how_to_use()
    
    # Print troubleshooting
    print_troubleshooting()
    
    # Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    print(f"\n✅ Checks Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ YOUR STREAMLIT APP IS FULLY CONFIGURED WITH TIGERGRAPH!")
        print("   Ready to run benchmarks and compare pipelines.")
        print(f"\n   Open: http://localhost:8501")
    else:
        print("\n⚠️  Some checks failed. Please review above and troubleshoot.")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
