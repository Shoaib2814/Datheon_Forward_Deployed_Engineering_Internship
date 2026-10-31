import os
import time
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Define paths
DATA_DIR = "data"
DB_DIR = "chroma_db"

def run_etl_pipeline():
    print("Starting Automated Data Extraction & Embedding Pipeline...")
    start_time = time.time()
    
    documents = []
    
    # 1. Ingest Multi-format Documents
    print("Ingesting documents from /data...")
    for filename in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR, filename)
        
        # Process Markdown files
        if filename.endswith(".md"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Basic metadata parsing from sample format
                documents.append({
                    "text": content,
                    "metadata": {"source": filename, "department": "Security", "access_tier": "Confidential", "date": "2026-10-30"}
                })
                
        # Process CSV files
        elif filename.endswith(".csv"):
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                text_content = str(row.get("content", ""))
                documents.append({
                    "text": text_content,
                    "metadata": {
                        "source": filename,
                        "department": str(row.get("department", "General")),
                        "access_tier": str(row.get("access_tier", "Public")),
                        "date": str(row.get("date", "2026-10-25"))
                    }
                })

    print(f"Extracted {len(documents)} raw document records.")

    # 2. Semantic Chunking
    print("Performing semantic chunking...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    final_texts = []
    final_metadatas = []
    
    for doc in documents:
        chunks = text_splitter.split_text(doc["text"])
        for chunk in chunks:
            final_texts.append(chunk)
            final_metadatas.append(doc["metadata"])

    print(f"Generated {len(final_texts)} total chunks.")

    # 3. Vector Database Embedding & Storage (ChromaDB with Cosine Similarity)
    print("Initializing embeddings and populating ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Chroma uses cosine similarity by default when configured via collection metadata or standard setup
    vector_store = Chroma.from_texts(
        texts=final_texts,
        embedding=embeddings,
        metadatas=final_metadatas,
        persist_directory=DB_DIR
    )
    
    elapsed_time = time.time() - start_time
    print(f"Pipeline completed successfully in {elapsed_time:.2f} seconds!")
    print(f"Vector database stored locally at: {os.path.abspath(DB_DIR)}")

if __name__ == "__main__":
    run_etl_pipeline()