import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

app = FastAPI()

# --- Data Loading ---
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

crm_data = load_data('crm.json')
billing_data = load_data('billing.json')
marketing_data = load_data('marketing.json')

# --- Pydantic Models ---
class DiscoveryRequest(BaseModel):
    email: EmailStr

# --- API Endpoints ---
@app.post("/discover")
async def discover_data(request: DiscoveryRequest):
    """
    Discovers personal data associated with a given email address
    across all connected data sources.
    """
    email_to_find = request.email.lower()
    findings = {
        "crm": [],
        "billing": [],
        "marketing": []
    }

    # Search CRM data
    for record in crm_data:
        if record.get("email", "").lower() == email_to_find:
            findings["crm"].append(record)

    # Search Billing data
    for record in billing_data:
        if record.get("user_email", "").lower() == email_to_find:
            findings["billing"].append(record)

    # Search Marketing data
    for record in marketing_data:
        if record.get("recipient_email", "").lower() == email_to_find:
            findings["marketing"].append(record)

    if not any(findings.values()):
        raise HTTPException(status_code=404, detail="No data found for the specified email address.")

    return findings

@app.get("/")
def read_root():
    return {"message": "Data Discovery Agent is running."}