import threading
import time
from src.mock_erp_server import app
from src.enterprise_agent import EnterpriseAgent

def run_server():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    # 1. Start the mock ERP/CRM server in a background thread
    print("Starting background Mock ERP Server...")
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Wait for server to initialize

    # 2. Initialize the Enterprise Agent
    agent = EnterpriseAgent()

    print("\n==================================================")
    print("TEST 1: Inventory Lookup & Automated Restock Ticket")
    print("==================================================")
    agent.run_task("Check GPU-A100 inventory and handle restocking if low.")

    print("\n==================================================")
    print("TEST 2: CRM Lead Status Update (Human-in-the-Loop)")
    print("==================================================")
    agent.run_task("Update lead status for LEAD-101.")