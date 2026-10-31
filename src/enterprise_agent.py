import requests
import time

BASE_URL = "http://localhost:5000/api"

class EnterpriseAgent:
    def __init__(self):
        print("Initializing Autonomous Enterprise Agent...")

    def lookup_inventory(self, item_id: str):
        """Read Operation: Looks up stock level and price."""
        print(f"\n[Tool: Inventory Lookup] Checking stock for item: {item_id}")
        try:
            response = requests.get(f"{BASE_URL}/inventory/{item_id}", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": response.json().get("message", "Item not found")}
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}

    def update_lead_status(self, lead_id: str, status: str):
        """Write Operation: Updates lead status in CRM (Requires Human Approval)."""
        print(f"\n[Tool: Lead Status Update] Attempting to update {lead_id} to '{status}'")
        
        # Human-in-the-Loop Confirmation Gate
        approval = input(f"⚠️ [HUMAN-IN-THE-LOOP APPROVAL] Authorize update for lead {lead_id} to '{status}'? (y/n): ").strip().lower()
        if approval != 'y':
            print("❌ Operation cancelled by supervisor.")
            return {"status": "cancelled", "message": "Write operation rejected by human."}

        try:
            response = requests.put(f"{BASE_URL}/leads/{lead_id}", json={"status": status}, timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}

    def create_support_ticket(self, subject: str, priority: str = "Normal"):
        """Write Operation: Creates a support/replenishment ticket (Requires Human Approval)."""
        print(f"\n[Tool: Ticket Creation] Attempting to create ticket: '{subject}' [{priority}]")
        
        # Human-in-the-Loop Confirmation Gate
        approval = input(f"⚠️ [HUMAN-IN-THE-LOOP APPROVAL] Authorize creation of ticket '{subject}'? (y/n): ").strip().lower()
        if approval != 'y':
            print("❌ Operation cancelled by supervisor.")
            return {"status": "cancelled", "message": "Write operation rejected by human."}

        try:
            response = requests.post(f"{BASE_URL}/tickets", json={"subject": subject, "priority": priority}, timeout=5)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection error: {str(e)}"}

    def run_task(self, goal: str):
        print(f"\n🤖 Agent Goal: {goal}")
        print("==============================================")
        print("--- Thought-Action-Observation Cycle Start ---")
        
        # Demonstration of Thought-Action Loop
        if "gpu" in goal.lower():
            # Thought 1: Check inventory
            print("Thought: I need to check the inventory level for GPU-A100.")
            obs = self.lookup_inventory("GPU-A100")
            print(f"Observation: {obs}")
            
            if "error" not in obs:
                stock = obs["data"]["stock"]
                print(f"Thought: Current stock is {stock}. If stock is below 20, I should trigger a replenishment ticket.")
                if stock < 20:
                    ticket_obs = self.create_support_ticket("Low stock alert for GPU-A100 - Restock Required", "High")
                    print(f"Observation: {ticket_obs}")
        
        elif "lead" in goal.lower():
            print("Thought: I need to update lead LEAD-101 status to 'Closed-Won'.")
            obs = self.update_lead_status("LEAD-101", "Closed-Won")
            print(f"Observation: {obs}")

        print("--- Thought-Action-Observation Cycle End ---")

if __name__ == "__main__":
    agent = EnterpriseAgent()
    # Test agent workflow
    agent.run_task("Check GPU-A100 inventory and handle restocking if low.")