#!/usr/bin/env python3
"""
Full Dataset Loader for TigerGraph GraphRAG
Prepares complete dataset for ingestion
"""
import sys
import os
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, os.path.abspath("."))

def analyze_full_dataset(filepath):
    """Analyze and prepare full dataset"""
    print("\n" + "="*70)
    print("FULL DATASET ANALYSIS FOR TIGERGRAPH GRAPHRAG")
    print("="*70)
    
    if not os.path.exists(filepath):
        print(f"✗ Dataset not found: {filepath}")
        sys.exit(1)
    
    # Get file statistics
    file_size = os.path.getsize(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
        total_words = len(content.split())
    
    # Token estimation
    estimated_tokens = int(total_words / 1.3)
    
    print(f"\n📊 DATASET STATISTICS:")
    print(f"  File Size: {file_size / 1024 / 1024:.2f} MB")
    print(f"  Total Lines: {len(lines):,}")
    print(f"  Total Words: {total_words:,}")
    print(f"  Estimated Tokens: {estimated_tokens:,}")
    print(f"  Hackathon Minimum: 2,000,000 tokens")
    print(f"  Status: {estimated_tokens / 2000000 * 100:.1f}% of requirement")
    
    return content, estimated_tokens

def prepare_documents(content, chunk_size=512):
    """Prepare documents for ingestion"""
    print(f"\n📝 PREPARING DOCUMENTS (chunk size: {chunk_size} tokens):")
    
    # Split by article
    articles = content.split('= ')
    articles = [f'= {a.strip()}' for a in articles if a.strip()]
    
    print(f"  Found {len(articles):,} articles")
    
    documents = []
    chunk_buffer = []
    chunk_tokens = 0
    
    for article in articles:
        article_tokens = len(article.split()) // 1.3
        
        if chunk_tokens + article_tokens > chunk_size and chunk_buffer:
            # Save current chunk
            doc = {
                "id": f"doc_{len(documents):06d}",
                "content": " ".join(chunk_buffer),
                "tokens": int(chunk_tokens),
                "created_at": datetime.now().isoformat()
            }
            documents.append(doc)
            chunk_buffer = []
            chunk_tokens = 0
        
        chunk_buffer.append(article)
        chunk_tokens += article_tokens
    
    # Add remaining
    if chunk_buffer:
        doc = {
            "id": f"doc_{len(documents):06d}",
            "content": " ".join(chunk_buffer),
            "tokens": int(chunk_tokens),
            "created_at": datetime.now().isoformat()
        }
        documents.append(doc)
    
    print(f"  Created {len(documents):,} documents")
    print(f"  Average doc size: ~{sum(d['tokens'] for d in documents) // len(documents)} tokens")
    
    return documents

def create_bulk_ingest_file(documents, output_file="data/bulk_ingest.jsonl"):
    """Create JSONL file for bulk ingestion"""
    print(f"\n💾 CREATING BULK INGEST FILE:")
    print(f"  Output: {output_file}")
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    total_tokens = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')
            total_tokens += doc['tokens']
    
    file_size = os.path.getsize(output_file)
    print(f"  Total Size: {file_size / 1024 / 1024:.2f} MB")
    print(f"  Total Tokens: {total_tokens:,}")
    print(f"  ✓ Ready for ingestion")
    
    return output_file, total_tokens

def create_csv_for_tigergraph(documents, output_file="data/documents.csv"):
    """Create CSV format for TigerGraph Data Loading"""
    print(f"\n📋 CREATING CSV FOR TIGERGRAPH:")
    print(f"  Output: {output_file}")
    
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    import csv
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Header
        writer.writerow(['document_id', 'content', 'token_count', 'created_at'])
        
        # Data rows
        for doc in documents:
            writer.writerow([
                doc['id'],
                doc['content'][:1000] + '...' if len(doc['content']) > 1000 else doc['content'],
                doc['tokens'],
                doc['created_at']
            ])
    
    file_size = os.path.getsize(output_file)
    print(f"  Total Size: {file_size / 1024:.2f} KB")
    print(f"  Total Documents: {len(documents):,}")
    print(f"  ✓ Ready for TigerGraph upload")
    
    return output_file

def print_loading_instructions():
    """Print instructions for loading into TigerGraph"""
    print("\n" + "="*70)
    print("LOADING INSTRUCTIONS FOR TIGERGRAPH")
    print("="*70)
    
    print("\n🔗 STEP 1: Open TigerGraph Admin Portal")
    print("   URL: https://tg-d30aafa4-669c-4606-b227-ae7da842e211.tg-3452941248.i.tgcloud.io:14240")
    print("   Username: sathiya")
    print("   Password: Mano@2611")
    
    print("\n📊 STEP 2: Create Graph Schema (if not exists)")
    print("   - Vertex types: Document, Entity, Concept")
    print("   - Edge types: mentions, related_to, extracted_from")
    
    print("\n📤 STEP 3: Load Data")
    print("   - Select graph: NexusRAG")
    print("   - Click 'Load Data'")
    print("   - Upload file: data/documents.csv")
    print("   - Map columns:")
    print("     * document_id → vertex ID")
    print("     * content → vertex attribute")
    print("     * token_count → vertex attribute")
    
    print("\n⏳ STEP 4: Monitor Progress")
    print("   - Watch the loading job status")
    print("   - Should complete in 5-15 minutes")
    
    print("\n✅ STEP 5: Verify Data")
    print("   - Check graph statistics")
    print("   - Run test queries via Query Editor")

def main():
    """Main function"""
    dataset_path = "data/dataset.txt"
    
    # Analyze dataset
    content, total_tokens = analyze_full_dataset(dataset_path)
    
    # Prepare documents
    documents = prepare_documents(content, chunk_size=512)
    
    # Create ingest files
    jsonl_file, total_tokens = create_bulk_ingest_file(documents)
    csv_file = create_csv_for_tigergraph(documents)
    
    # Print instructions
    print_loading_instructions()
    
    # Summary
    print("\n" + "="*70)
    print("✓ DATASET PREPARATION COMPLETE")
    print("="*70)
    print(f"\nFiles created:")
    print(f"  ✓ {csv_file} - For TigerGraph upload")
    print(f"  ✓ {jsonl_file} - Alternative bulk format")
    print(f"\nNext: Upload {csv_file} via TigerGraph Admin Portal")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
