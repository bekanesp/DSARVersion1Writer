# Request Intake Service

This service is the public-facing component of the DSR Automation Platform. It provides a simple web UI and a REST API for data subjects to submit Data Subject Requests (DSRs).

## API

*   `POST /requests`: Programmatically submits a DSR.
*   `GET /`: Serves an HTML form to submit a DSR through a web browser.
*   `POST /submit`: Handles the form submission from the UI.

**Request Body for `POST /requests`:**

```json
{
    "email": "user@example.com",
    "request_type": "access"
}
```

**Supported Request Types:** `access`, `deletion`, `correction`.

**Success Response:**

```json
{
    "message": "Request received and is being processed.",
    "request_id": "req_1"
}
```

## Features

*   **Data Validation:** Uses Pydantic to ensure that submitted data (like email format) is valid.
*   **Identity Verification (Simulated):** Includes a placeholder for sending a verification email to the data subject.
*   **Workflow Integration (Simulated):** Includes a placeholder for calling the Workflow Orchestration Engine to kick off the DSR fulfillment process.

## How to Run

1.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  Start the service:
    ```bash
    uvicorn main:app --reload
    ```
The service will be available at `http://127.0.0.1:8000`.