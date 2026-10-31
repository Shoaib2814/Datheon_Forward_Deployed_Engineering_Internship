from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock Database
INVENTORY = {
    "GPU-A100": {"stock": 15, "price": 12000, "warehouse": "North-Hub"},
    "GPU-H100": {"stock": 4, "price": 25000, "warehouse": "South-Hub"}
}

LEADS = {
    "LEAD-101": {"name": "Acme Corp", "status": "Prospect"},
    "LEAD-102": {"name": "Globex", "status": "Negotiation"}
}

TICKETS = []

@app.route("/api/inventory/<item_id>", methods=["GET"])
def get_inventory(item_id):
    """Read Operation: Inventory Lookup"""
    item = INVENTORY.get(item_id.upper())
    if item:
        return jsonify({"status": "success", "item": item_id.upper(), "data": item})
    return jsonify({"status": "error", "message": "Item not found in inventory"}), 404

@app.route("/api/leads/<lead_id>", methods=["PUT"])
def update_lead(lead_id):
    """Write Operation: Lead Status Update"""
    data = request.json
    new_status = data.get("status")
    if lead_id in LEADS:
        LEADS[lead_id]["status"] = new_status
        return jsonify({"status": "success", "message": f"Lead {lead_id} status updated to {new_status}", "lead": LEADS[lead_id]})
    return jsonify({"status": "error", "message": "Lead ID not found"}), 404

@app.route("/api/tickets", methods=["POST"])
def create_ticket():
    """Write Operation: Support/Service Ticket Creation"""
    data = request.json
    subject = data.get("subject")
    priority = data.get("priority", "Normal")
    ticket_id = f"TICK-{len(TICKETS) + 1001}"
    ticket = {"ticket_id": ticket_id, "subject": subject, "priority": priority, "status": "Open"}
    TICKETS.append(ticket)
    return jsonify({"status": "success", "message": "Ticket created successfully", "ticket": ticket})

if __name__ == "__main__":
    print("Starting Mock Enterprise ERP/CRM Server on port 5000...")
    app.run(port=5000, debug=False)