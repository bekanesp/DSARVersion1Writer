import httpx
import time

# --- Configuration ---
ORCHESTRATION_ENGINE_URL = "http://127.0.0.1:8003" # Should match the port in the service's README
TEST_EMAIL = "alice@example.com" # An email that exists in the mock data
MAX_RETRIES = 5
RETRY_DELAY = 5 # seconds

def check_service_health(client, service_name, url):
    """Checks if a service is responsive."""
    print(f"Checking health of {service_name} at {url}...")
    try:
        response = client.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{service_name} is up and running.")
            return True
        else:
            print(f"{service_name} returned status {response.status_code}.")
            return False
    except httpx.ConnectError:
        print(f"Could not connect to {service_name}.")
        return False

def run_test():
    """
    Runs a simple end-to-end integration test with retries.
    """
    print("--- Starting Integration Test ---")

    with httpx.Client(timeout=30.0) as client:
        # Wait for the main service to be ready
        for i in range(MAX_RETRIES):
            if check_service_health(client, "Workflow Orchestration Engine", ORCHESTRATION_ENGINE_URL):
                break
            if i < MAX_RETRIES - 1:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
        else:
            print("\n--- Integration Test Failed! ---")
            print("Workflow Orchestration Engine did not become available in time.")
            return

    # Step 1: Define the request payload
    payload = {
        "email": TEST_EMAIL,
        "request_type": "access"
    }
    print(f"Submitting DSR for: {TEST_EMAIL}")

    # Step 2: Call the Workflow Orchestration Engine to start the process
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(f"{ORCHESTRATION_ENGINE_URL}/workflows/start", json=payload)
            
            # Check for a successful response
            if response.status_code == 200:
                print("Workflow started successfully!")
                result = response.json()
                print("\n--- Workflow Result ---")
                print(f"Request ID: {result.get('request_id')}")
                print(f"Message: {result.get('message')}")
                
                delivery_details = result.get('delivery_details', {})
                print("\n--- Delivery Details ---")
                print(f"Download URL: {delivery_details.get('download_url')}")
                print(f"Password: {delivery_details.get('password')}")
                
                print("\n--- Integration Test Passed! ---")
            else:
                print(f"\n--- Integration Test Failed! ---")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")

    except httpx.ConnectError as e:
        print("\n--- Integration Test Failed! ---")
        print("Connection Error: Could not connect to the Workflow Orchestration Engine.")
        print("Please ensure all services are running on their configured ports:")
        print("- Request Intake Service: 8000")
        print("- Data Discovery Agent: 8001")
        print("- Secure Delivery Service: 8002")
        print("- Workflow Orchestration Engine: 8003")
    except Exception as e:
        print(f"\n--- An unexpected error occurred: {e} ---")

if __name__ == "__main__":
    # Give the services a moment to start up if run immediately after launch
    time.sleep(2) 
    run_test()