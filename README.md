# Datheon Forward Deployed Engineering Internship

## Task 1: Automated Data Extraction & Embedding Pipeline
- Ingests multi-format documents (Markdown, CSV).
- Performs semantic chunking with metadata preservation (department, access tier, date).
- Stores vector embeddings in ChromaDB with cosine similarity indexes.

## Task 2: Production-Grade Secure RAG Engine
- **Strict RBAC Enforcement**: Automatically restricts document retrieval based on user clearance tiers (`Public`, `Internal`, `Tier-2`, `Tier-1`).
- **Query Re-writing**: Refines user queries for better vector search accuracy.
- **Cross-Encoder Re-ranking**: Uses `ms-marco-MiniLM-L-6-v2` to precisely re-rank retrieved chunks.
- **Source Citations**: Returns guardrailed responses with verifiable source page numbers and clearance details.

### Project Structure