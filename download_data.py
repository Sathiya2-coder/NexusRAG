import os
from datasets import load_dataset
import tiktoken

def main():
    print("Downloading WikiText-2 dataset...")
    # wikitext-2-raw-v1 has roughly 2 million words, perfectly fitting the hackathon requirement
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    
    os.makedirs("data", exist_ok=True)
    output_file = "data/dataset.txt"
    
    print(f"Saving to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        for item in dataset:
            text = item['text'].strip()
            if text:
                f.write(text + "\n")
                
    print("File saved. Counting tokens...")
    enc = tiktoken.get_encoding("cl100k_base")
    
    with open(output_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    tokens = enc.encode(content)
    print(f"Total tokens in dataset: {len(tokens):,}")
    print("Done!")

if __name__ == "__main__":
    main()
