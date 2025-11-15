import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from enum import Enum
import datetime

app = FastAPI()

# --- Service URLs ---
# In a real microservices architecture, these would be discovered via a service registry
# or configured via environment variables.
DATA_DISCOVERY_AGENT_URL = "http://localhost:8001"  # Assuming it runs on a different port
SECURE_DELIVERY_SERVICE_URL = "http://localhost:8002"

# --- Enums and Models ---
class DSRRequestType(str, Enum):
    ACCESS = "access"
    DELETION = "deletion"

class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DATA_DISCOVERY_COMPLETE = "DATA_DISCOVERY_COMPLETE"
    DELIVERY_COMPLETE = "DELIVERY_COMPLETE"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"

class WorkflowStartRequest(BaseModel):
    email: EmailStr
    request_type: DSRRequestType

# In-memory storage for workflows. In a real app, use a database.
workflows_db = {}
audit_log = []

def log_event(request_id: str, event: str):
    """Adds an entry to the audit log."""
    timestamp = datetime.datetime.utcnow().isoformat()
    audit_log.append(f"{timestamp} - Request {request_id}: {event}")
    print(f"AUDIT: {timestamp} - Request {request_id}: {event}")

# --- API Endpoints ---
@app.post("/workflows/start")
async def start_workflow(request: WorkflowStartRequest):
    """
    Starts the DSR fulfillment workflow.
    """
    request_id = f"wf_{len(workflows_db) + 1}"
    workflows_db[request_id] = {
        "status": WorkflowStatus.PENDING,
        "details": request.dict()
    }
    log_event(request_id, "Workflow started.")

    async with httpx.AsyncClient() as client:
        # Step 1: Call Data Discovery Agent
        try:
            workflows_db[request_id]["status"] = WorkflowStatus.IN_PROGRESS
            log_event(request_id, "Calling Data Discovery Agent.")
            
            response = await client.post(
                f"{DATA_DISCOVERY_AGENT_URL}/discover",
                json={"email": request.email}
            )
            response.raise_for_status()
            discovered_data = response.json()
            
            workflows_db[request_id]["status"] = WorkflowStatus.DATA_DISCOVERY_COMPLETE
            workflows_db[request_id]["discovered_data"] = discovered_data
            log_event(request_id, "Data discovery successful.")

        except httpx.RequestError as e:
            workflows_db[request_id]["status"] = WorkflowStatus.FAILED
            log_event(request_id, f"Failed to connect to Data Discovery Agent: {e}")
            raise HTTPException(status_code=503, detail="Data Discovery Agent is unavailable.")
        except httpx.HTTPStatusError as e:
            workflows_db[request_id]["status"] = WorkflowStatus.FAILED
            log_event(request_id, f"Data Discovery Agent returned an error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from Data Discovery Agent: {e.response.text}")

        # Step 2: Call Secure Delivery Service
        try:
            log_event(request_id, "Calling Secure Delivery Service.")
            
            delivery_payload = {
                "data": discovered_data,
                "email": request.email
            }
            response = await client.post(
                f"{SECURE_DELIVERY_SERVICE_URL}/delivery/create",
                json=delivery_payload
            )
            response.raise_for_status()
            delivery_info = response.json()
            
            workflows_db[request_id]["status"] = WorkflowStatus.DELIVERY_COMPLETE
            workflows_db[request_id]["delivery_info"] = delivery_info
            log_event(request_id, "Secure delivery package created.")

        except httpx.RequestError as e:
            workflows_db[request_id]["status"] = WorkflowStatus.FAILED
            log_event(request_id, f"Failed to connect to Secure Delivery Service: {e}")
            raise HTTPException(status_code=503, detail="Secure Delivery Service is unavailable.")
        except httpx.HTTPStatusError as e:
            workflows_db[request_id]["status"] = WorkflowStatus.FAILED
            log_event(request_id, f"Secure Delivery Service returned an error: {e.response.text}")
            raise HTTPException(status_code=e.response.status_code, detail=f"Error from Secure Delivery Service: {e.response.text}")

    workflows_db[request_id]["status"] = WorkflowStatus.COMPLETE
    log_event(request_id, "Workflow completed successfully.")
    
    return {
        "message": "Workflow completed successfully.",
        "request_id": request_id,
        "delivery_details": delivery_info
    }

@app.get("/workflows/{request_id}")
def get_workflow_status(request_id: str):
    """
    Retrieves the status and details of a specific workflow.
    """
    if request_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found.")
    return workflows_db[request_id]

@app.get("/auditlog")
def get_audit_log():
    """
    Returns the complete audit log.
    """
    return {"audit_log": audit_log}

@app.get("/")
def read_root():
    return {"message": "Workflow Orchestration Engine is running."}