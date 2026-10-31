from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DB_DIR = "chroma_db"

def test_vector_search():
    print("Loading vector store...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    query = "What are the encryption requirements?"
    print(f"\nQuery: '{query}'")
    
    # Search without filter
    results = vector_store.similarity_search(query, k=2)
    print("\n--- Search Results (No Filter) ---")
    for r in results:
        print(f"- [Dept: {r.metadata.get('department')}] {r.page_content}")
        
    # Search with metadata filter
    print("\n--- Search Results (Filtered: Department = Security) ---")
    filtered_results = vector_store.similarity_search(
        query, 
        k=2, 
        filter={"department": "Security"}
    )
    for r in filtered_results:
        print(f"- [Dept: {r.metadata.get('department')}] {r.page_content}")

if __name__ == "__main__":
    test_vector_search()