# DSR Automation Platform

This project is a fully functional, multi-component DSR (Data Subject Request) Automation Platform. It is architected as a set of four interconnected microservices that manage the end-to-end DSR lifecycle.

## 1. Project Overview

Organizations worldwide are required to fulfill Data Subject Requests (DSRs) under regulations like GDPR and CCPA. This platform automates the process, from the initial request intake to the final secure delivery of data.

## 2. Core Components

The platform consists of four microservices:

*   **Request Intake Service:** A public-facing service to receive and validate DSRs.
*   **Data Discovery Agent:** An internal service that connects to data sources and finds personal data.
*   **Workflow Orchestration Engine:** The central brain that manages the entire DSR fulfillment process.
*   **Secure Delivery Service:** A service dedicated to the secure packaging and delivery of the final data export.

Each service is a self-contained application with a clear API for communication. You can find detailed information about each service in its respective `README.md` file.

## 3. How to Run the Platform

**Prerequisites:**

*   Python 3.9+
*   `pip` for package installation
*   The `zip` command-line utility (for the Secure Delivery Service)

**Running the Services:**

Since Docker is not available in the execution environment, the services must be run as individual background processes.

1.  **Install Dependencies for All Services:**
    Navigate to the root `dsr_automation_platform` directory and run:
    ```bash
    pip install -r request_intake_service/requirements.txt
    pip install -r data_discovery_agent/requirements.txt
    pip install -r secure_delivery_service/requirements.txt
    pip install -r workflow_orchestration_engine/requirements.txt
    ```

2.  **Start Each Service in a Separate Terminal:**
    Open four separate terminals and run the following commands, one in each terminal:

    *   **Terminal 1: Request Intake Service**
        ```bash
        cd request_intake_service
        uvicorn main:app --host 0.0.0.0 --port 8000
        ```
    *   **Terminal 2: Data Discovery Agent**
        ```bash
        cd data_discovery_agent
        uvicorn main:app --host 0.0.0.0 --port 8001
        ```
    *   **Terminal 3: Secure Delivery Service**
        ```bash
        cd secure_delivery_service
        uvicorn main:app --host 0.0.0.0 --port 8002
        ```
    *   **Terminal 4: Workflow Orchestration Engine**
        ```bash
        cd workflow_orchestration_engine
        uvicorn main:app --host 0.0.0.0 --port 8003
        ```

## 4. Running the Integration Test

With all four services running, you can run the integration test to verify the end-to-end workflow.

In a new terminal, from the root `dsr_automation_platform` directory, run:
```bash
python test_integration.py
```
A successful test will print a "--- Integration Test Passed! ---" message.

## 5. Security & Compliance

*   **No Data in Email:** Personal data files are never sent via email.
*   **Encryption:** All data packages are encrypted in a password-protected ZIP file.
*   **Authentication:** The final download step is gated by a re-authentication challenge (simulated).
*   **Auditability:** Every significant action is logged by the Workflow Orchestration Engine.