# Data Discovery Agent

This service is a component of the DSR Automation Platform. Its purpose is to connect to data sources and find personal data related to a specific identity.

## API

The service exposes a single endpoint:

*   `POST /discover`: Accepts a JSON payload with an email address and returns a JSON report of all findings.

**Request Body:**

```json
{
    "email": "user@example.com"
}
```

**Success Response (200 OK):**

```json
{
    "crm": [
        {
            "id": "user-123",
            "email": "user@example.com",
            ...
        }
    ],
    "billing": [
        {
            "transaction_id": "txn-abc",
            "user_email": "user@example.com",
            ...
        }
    ],
    "marketing": []
}
```

**Error Response (404 Not Found):**

```json
{
    "detail": "No data found for the specified email address."
}
```

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