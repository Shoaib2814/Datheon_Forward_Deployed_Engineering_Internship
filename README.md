# Automated Data Extraction & Vector Embedding ETL Pipeline

## Project Overview
An automated ETL (Extract, Transform, Load) pipeline designed to ingest multi-format client documents, perform semantic chunking with metadata preservation (department, access tier, date), and persist vector embeddings into ChromaDB with cosine similarity indexing.

## Features
- **Multi-Format Ingestion:** Supports CSV and Markdown file processing.
- **Semantic Chunking:** Context-aware text splitting preserving department, access tier, and date metadata.
- **Vector Database (ChromaDB):** Persistent local vector store utilizing cosine similarity.
- **Batch Ingestion Benchmarking:** Measures throughput performance and processing duration during ingestion batches.
- **Metadata Filtering:** Retrieves precise documents based on metadata attributes (e.g., department-specific filtering).

## Project Structure
```text
Datheon_Forward_Deployed_Engineering_Internship/
├── data/
│   ├── Finance_Report.csv
│   └── Tech_Docs.md
├── chroma_db/
├── etl_pipeline.py
├── requirements.txt
└── README.md