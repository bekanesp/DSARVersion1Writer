from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr
from enum import Enum

app = FastAPI()

# --- Enums and Models ---
class DSRRequestType(str, Enum):
    ACCESS = "access"
    DELETION = "deletion"
    CORRECTION = "correction"

class DSRRequest(BaseModel):
    email: EmailStr
    request_type: DSRRequestType
    request_details: str = None

# In-memory storage for requests. In a real app, use a database.
requests_db = {}

# --- API Endpoints ---
@app.post("/requests")
async def submit_dsr_request(request: DSRRequest):
    """
    API endpoint to programmatically submit a DSR.
    """
    # 1. Validation is handled by Pydantic
    
    # 2. Perform basic identity verification (simulation)
    # In a real app, this would involve sending an email with a verification link.
    print(f"Received DSR Request: Email='{request.email}', Type='{request.request_type}'")
    print("Simulating identity verification...")
    
    # 3. Queue the request and call the Workflow Orchestration Engine
    # This is a placeholder for the call to the next service.
    print("Calling Workflow Orchestration Engine to start the process...")
    
    request_id = f"req_{len(requests_db) + 1}"
    requests_db[request_id] = request.dict()
    
    return {"message": "Request received and is being processed.", "request_id": request_id}

# --- Web UI ---
@app.get("/", response_class=HTMLResponse)
async def get_request_form():
    """
    Serves a simple HTML form for submitting DSRs.
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Submit DSR</title>
    </head>
    <body>
        <h1>Data Subject Request (DSR)</h1>
        <form action="/submit" method="post">
            <label for="email">Your Email:</label><br>
            <input type="email" id="email" name="email" required><br><br>
            
            <label for="request_type">Request Type:</label><br>
            <select id="request_type" name="request_type">
                <option value="access">Access My Data</option>
                <option value="deletion">Delete My Data</option>
                <option value="correction">Correct My Data</option>
            </select><br><br>
            
            <label for="request_details">Details (for correction):</label><br>
            <textarea id="request_details" name="request_details" rows="4" cols="50"></textarea><br><br>
            
            <input type="submit" value="Submit Request">
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/submit")
async def handle_form_submission(
    email: EmailStr = Form(...),
    request_type: DSRRequestType = Form(...),
    request_details: str = Form(None)
):
    """
    Handles the submission from the HTML form.
    """
    dsr_request = DSRRequest(
        email=email,
        request_type=request_type,
        request_details=request_details
    )
    return await submit_dsr_request(dsr_request)

@app.get("/status")
def get_status():
    return {"message": "Request Intake Service is running."}