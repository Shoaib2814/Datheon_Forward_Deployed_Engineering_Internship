from src.rag_engine import SecureRAGEngine

def run_tests():
    engine = SecureRAGEngine()
    
    print("\n==============================================")
    print("TEST 1: Tier-1 User Query (Full Access)")
    print("==============================================")
    ans1 = engine.query("What are the encryption requirements and budget?", user_clearance_tier="Tier-1")
    print("\n=== Final Output (Tier-1) ===")
    print(ans1)
    
    print("\n==============================================")
    print("TEST 2: Public User Query (Restricted Access)")
    print("==============================================")
    ans2 = engine.query("What are the encryption requirements and budget?", user_clearance_tier="Public")
    print("\n=== Final Output (Public) ===")
    print(ans2)

if __name__ == "__main__":
    run_tests()