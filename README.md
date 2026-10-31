# Datheon Forward Deployed Engineering Internship

## Task 1: Automated Data Extraction & Embedding Pipeline
- Ingests multi-format documents (Markdown, CSV).
- Performs semantic chunking with metadata preservation.
- Stores vector embeddings in ChromaDB with cosine similarity indexes.

## Task 2: Production-Grade Secure RAG Engine
- **Strict RBAC Enforcement**: Automatically restricts document retrieval based on user clearance tiers.
- **Query Re-writing & Cross-Encoder Re-ranking**: Uses `ms-marco-MiniLM-L-6-v2` for high-precision retrieval and citations.

## Task 3: Autonomous Enterprise Agent with Tool-Calling & HITL
- **Mock ERP/CRM REST Endpoints**: Implements endpoints for inventory lookup, lead status updates, and support ticket creation.
- **Thought-Action-Observation Loops**: Autonomous agent reasoning cycles for enterprise workflows.
- **Human-in-the-Loop (HITL) Validation Gates**: Requires explicit supervisor authorization (`y/n`) before executing sensitive write operations (`PUT`/`POST`).

### Project Structure