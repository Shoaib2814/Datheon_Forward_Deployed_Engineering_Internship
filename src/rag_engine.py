import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

DB_DIR = "chroma_db"

class SecureRAGEngine:
    def __init__(self):
        print("Initializing Secure RAG Engine...")
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(persist_directory=DB_DIR, embedding_function=self.embeddings)
        
        # Load Cross-Encoder for precise re-ranking
        print("Loading Cross-Encoder re-ranker...")
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    def rewrite_query(self, user_query: str) -> str:
        """Simple query re-writing / expansion for better vector matching"""
        rewritten = user_query.strip()
        if not rewritten.endswith("?"):
            rewritten += "?"
        return rewritten

    def query(self, user_query: str, user_clearance_tier: str, top_k: int = 3):
        """
        Executes secure RAG query with strict RBAC filtering and Cross-Encoder re-ranking.
        """
        print(f"\n--- Processing Query: '{user_query}' [User Clearance: {user_clearance_tier}] ---")
        
        # 1. Query Re-writing
        refined_query = self.rewrite_query(user_query)
        print(f"[1] Refined Query: {refined_query}")
        
        # 2. Strict RBAC Enforcement via Metadata Filtering
        # Depending on user tier, allow matching access tiers
        allowed_tiers = ["Public"]
        if user_clearance_tier == "Tier-2":
            allowed_tiers.extend(["Tier-2", "Internal"])
        elif user_clearance_tier == "Tier-1":
            allowed_tiers.extend(["Tier-1", "Tier-2", "Internal", "Confidential"])

        # Retrieve candidates from ChromaDB
        # Note: Chroma filtering syntax
        raw_docs = self.vector_store.similarity_search(refined_query, k=top_k * 2)
        
        # Filter by RBAC clearance locally or via metadata filter
        filtered_docs = []
        for doc in raw_docs:
            doc_tier = doc.metadata.get("access_tier", "Public")
            if doc_tier in allowed_tiers or user_clearance_tier == "Tier-1":
                filtered_docs.append(doc)

        if not filtered_docs:
            return "Access Denied or No Relevant Information Found under your clearance level."

        print(f"[2] Retrieved {len(filtered_docs)} documents passing RBAC.")

        # 3. Cross-Encoder Re-ranking
        pairs = [[refined_query, doc.page_content] for doc in filtered_docs]
        scores = self.reranker.predict(pairs)
        
        # Sort documents by cross-encoder score descending
        scored_docs = sorted(zip(filtered_docs, scores), key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, score in scored_docs[:top_k]]

        print(f"[3] Re-ranked top {len(top_docs)} results using Cross-Encoder.")

        # 4. Construct Guardrailed Response with Citations
        context_blocks = []
        for i, doc in enumerate(top_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("page", "1")
            tier = doc.metadata.get("access_tier", "Public")
            context_blocks.append(f"Source [{i}]: {source} (Page {page}, Clearance: {tier})\nContent: {doc.page_content}")

        response_summary = f"Based on authorized internal documents:\n\n" + "\n\n".join(context_blocks)
        return response_summary

if __name__ == "__main__":
    engine = SecureRAGEngine()
    # Test query
    ans = engine.query("What is the budget allocation for AI?", user_clearance_tier="Tier-1")
    print("\n=== Final Answer ===")
    print(ans)