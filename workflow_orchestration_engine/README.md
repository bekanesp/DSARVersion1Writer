# Workflow Orchestration Engine

This service is the central brain of the DSR Automation Platform. It manages the entire DSR fulfillment process from start to finish.

## API

*   `POST /workflows/start`: Kicks off the DSR fulfillment workflow.
*   `GET /workflows/{request_id}`: Retrieves the status of a specific workflow.
*   `GET /auditlog`: Returns the complete audit log of all actions taken by the engine.

**Request Body for `POST /workflows/start`:**

```json
{
    "email": "user@example.com",
    "request_type": "access"
}
```

**Success Response:**

```json
{
    "message": "Workflow completed successfully.",
    "request_id": "wf_1",
    "delivery_details": {
        "message": "Secure delivery package created.",
        "download_url": "/delivery/download/some-unique-token",
        "password": "a-very-secure-password"
    }
}
```

## Workflow Logic

1.  Receives a verified request from the Request Intake Service (or a direct API call).
2.  Calls the **Data Discovery Agent** to find all personal data for the given email.
3.  Once data is received, it calls the **Secure Delivery Service** to package and host the data.
4.  Manages the status of the request (e.g., `PENDING`, `IN_PROGRESS`, `COMPLETE`).
5.  Maintains a detailed audit log for every step of the process.

## How to Run

1.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure the other services (Data Discovery and Secure Delivery) are running on their configured ports.
3.  Start the service:
    ```bash
    uvicorn main:app --reload --port 8003 
    ```
    *(Note: This service should run on a different port than the others, e.g., 8003)*

The service will be available at `http://127.0.0.1:8003`.