import json
import os
import secrets
import subprocess
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI()

# In-memory storage for delivery links. In a real app, use a database.
delivery_links: Dict[str, Dict[str, Any]] = {}
STORAGE_PATH = "secure_storage"

# --- Pydantic Models ---
class DeliveryRequest(BaseModel):
    data: Dict[str, Any]
    email: str

# --- Helper Functions ---
def create_encrypted_zip(data: Dict[str, Any], email: str) -> (str, str):
    """Creates a password-protected ZIP file with the user's data."""
    password = secrets.token_urlsafe(16)
    request_id = str(uuid.uuid4())
    
    json_filename = f"{request_id}.json"
    zip_filename = f"{request_id}.zip"
    
    json_filepath = os.path.join(STORAGE_PATH, json_filename)
    zip_filepath = os.path.join(STORAGE_PATH, zip_filename)

    # Write data to a temporary JSON file
    with open(json_filepath, 'w') as f:
        json.dump(data, f, indent=4)

    # Create a password-protected ZIP file using the zip command
    # The -P flag sets the password. -j jits the path.
    subprocess.run(
        ["zip", "-j", "-P", password, zip_filepath, json_filepath],
        check=True
    )

    # Clean up the temporary JSON file
    os.remove(json_filepath)

    return zip_filepath, password

# --- API Endpoints ---
@app.post("/delivery/create")
async def create_delivery(request: DeliveryRequest):
    """
    Packages data into an encrypted ZIP and creates a secure download link.
    """
    zip_filepath, password = create_encrypted_zip(request.data, request.email)
    
    token = str(uuid.uuid4())
    delivery_links[token] = {
        "file_path": zip_filepath,
        "password": password,
        "email": request.email
    }
    
    # In a real application, you would send an email with the download_url
    # and a separate communication for the password.
    # For this simulation, we return them directly.
    download_url = f"/delivery/download/{token}"
    
    return {
        "message": "Secure delivery package created.",
        "download_url": download_url,
        "password": password # WARNING: For simulation only. Do not do this in production.
    }

@app.get("/delivery/download/{token}", response_class=HTMLResponse)
async def download_portal(token: str):
    """
    Serves a download portal page. In a real app, this would
    require re-authentication.
    """
    if token not in delivery_links:
        raise HTTPException(status_code=404, detail="Download link is invalid or has expired.")
    
    # Simple HTML page with a download button and password display
    # In a real app, you would have a form to enter a 2FA code before showing this.
    delivery_info = delivery_links[token]
    password = delivery_info["password"]
    download_link = f"/delivery/download_file/{token}"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Secure Download</title>
    </head>
    <body>
        <h1>Secure Data Download</h1>
        <p>Your data package is ready for download. Please use the password below to decrypt the ZIP file after downloading.</p>
        <p><strong>Password:</strong> <code>{password}</code></p>
        <a href="{download_link}" download>
            <button>Download Data Package</button>
        </a>
        <p><small>This link is valid for a limited time.</small></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/delivery/download_file/{token}")
async def download_file(token: str):
    """Serves the actual encrypted ZIP file."""
    if token not in delivery_links:
        raise HTTPException(status_code=404, detail="Download link is invalid or has expired.")
    
    file_path = delivery_links[token]["file_path"]
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
        
    return FileResponse(path=file_path, filename=os.path.basename(file_path))

@app.get("/")
def read_root():
    return {"message": "Secure Delivery Service is running."}