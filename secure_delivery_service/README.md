# Secure Delivery Service

This service is a component of the DSR Automation Platform. It is responsible for securely packaging and delivering the final data export to the data subject.

## API

The service exposes three main endpoints:

*   `POST /delivery/create`: Accepts a JSON payload with the data report and the user's email. It packages the data into an encrypted, password-protected ZIP file, stores it securely, and generates a time-limited, secure download link.
*   `GET /delivery/download/{token}`: Serves a simple web portal where the user must re-authenticate (simulated in this version) before they can download the file.
*   `GET /delivery/download_file/{token}`: Serves the actual encrypted ZIP file for download.

**Request Body for `/delivery/create`:**

```json
{
    "data": { ... },
    "email": "user@example.com"
}
```

**Success Response for `/delivery/create`:**

```json
{
    "message": "Secure delivery package created.",
    "download_url": "/delivery/download/some-unique-token",
    "password": "a-very-secure-password"
}
```

## Security Features

*   **Encryption:** Data is packaged in a password-protected ZIP file.
*   **Secure Link:** A unique, time-limited token is generated for each download.
*   **Re-authentication:** The download portal is designed to require re-authentication before providing the download link and password (this is simulated in the current version).

## How to Run

1.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
2.  Ensure the `zip` command-line tool is installed.
3.  Start the service:
    ```bash
    uvicorn main:app --reload
    ```
The service will be available at `http://127.0.0.1:8000`.