# NexusRAG Platform

NexusRAG is a high-performance benchmark dashboard built for the GraphRAG Hackathon Government Division. It compares traditional LLM inference, Basic RAG, and GraphRAG architectures side-by-side.

## Features
- **Benchmark Dashboard**: Compares pipelines live using Groq's Llama-3 API.
- **AI Judge Verdict**: Uses an LLM-as-a-judge to evaluate pipeline answers.
- **Data Explorer**: View and download the raw WikiText-2 dataset.
- **Workflow**: Detailed architecture diagrams and explanations.

## Setup
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run `python download_data.py` to fetch the dataset.
4. Set your `GROQ_API_KEY` in a `.env` file.
5. Run the app: `streamlit run app.py`
