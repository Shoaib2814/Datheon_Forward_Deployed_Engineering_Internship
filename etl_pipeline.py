import os
import time
import csv
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

# --- Configuration ---
DATA_DIR = "./data"
CHROMA_DB_DIR = "./chroma_db"

# 1. Multi-Format Data Ingestion (Using Built-in CSV Reader)
def load_documents(data_dir: str) -> List[Document]:
    documents = []
    print(f"[*] Ingesting documents from '{data_dir}'...")
    
    if not os.path.exists(data_dir):
        print(f"[!] Directory '{data_dir}' not found. Please create it and add files.")
        return documents

    for root, _, files in os.walk(data_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Markdown Loader
            if file.endswith(".md"):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                doc = Document(
                    page_content=content,
                    metadata={"department": "Engineering", "access_tier": "Tier-1", "date": "2026-10-10", "source": file_path}
                )
                documents.append(doc)
                
            # CSV Loader (Using Built-in CSV module)
            elif file.endswith(".csv"):
                with open(file_path, mode="r", encoding="utf-8") as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    for row in csv_reader:
                        doc = Document(
                            page_content=str(row.get("Content", "")),
                            metadata={
                                "department": str(row.get("Department", "General")),
                                "access_tier": str(row.get("AccessTier", "Tier-3")),
                                "date": str(row.get("Date", "2026-01-01")),
                                "source": file_path
                            }
                        )
                        documents.append(doc)
                    
    print(f"[+] Loaded {len(documents)} raw documents/records.")
    return documents

# 2. Semantic Chunking
def chunk_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"[+] Created {len(chunks)} semantic chunks with preserved metadata.")
    return chunks

# 3. Vector Database Ingestion & Benchmarking
def ingest_and_benchmark(chunks: List[Document], batch_size: int = 5):
    print("\n[*] Initializing ChromaDB Vector Database...")
    
    start_time = time.time()
    
    # ChromaDB Vectorstore with default local embedding
    vectorstore = Chroma(
        collection_name="client_docs",
        persist_directory=CHROMA_DB_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )
    
    total_chunks = len(chunks)
    print(f"[*] Starting Batch Ingestion (Batch Size: {batch_size})...")
    
    for i in range(0, total_chunks, batch_size):
        batch = chunks[i:i + batch_size]
        batch_start = time.time()
        vectorstore.add_documents(batch)
        batch_end = time.time()
        print(f"    - Ingested batch {i // batch_size + 1} ({len(batch)} items) in {batch_end - batch_start:.4f} sec")

    total_time = time.time() - start_time
    print(f"\n[✔] Ingestion Complete! Total Time: {total_time:.2f} seconds.")
    print(f"[✔] Throughput: {total_chunks / total_time:.2f} chunks/sec")
    return vectorstore

# 4. Metadata Filtering Query Demo
def test_metadata_filtering(vectorstore):
    print("\n" + "="*50)
    print("[*] Testing Metadata Filtering Queries:")
    print("="*50)
    
    query = "Budget allocation"
    filter_criteria = {"department": "Finance"}
    
    print(f"Query: '{query}' | Filter: {filter_criteria}")
    results = vectorstore.similarity_search(query, k=2, filter=filter_criteria)
    
    for idx, doc in enumerate(results, 1):
        print(f"\nResult #{idx}:")
        print(f"Content: {doc.page_content}")
        print(f"Metadata: {doc.metadata}")

if __name__ == "__main__":
    raw_docs = load_documents(DATA_DIR)
    if raw_docs:
        chunked_docs = chunk_documents(raw_docs)
        db = ingest_and_benchmark(chunked_docs, batch_size=2)
        test_metadata_filtering(db)