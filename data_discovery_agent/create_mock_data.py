import json

# Data for crm.json
crm_data = [
    {
        "id": "user-123",
        "email": "alice@example.com",
        "firstName": "Alice",
        "lastName": "Smith",
        "phone": "123-456-7890",
        "createdAt": "2023-01-15T10:30:00Z"
    },
    {
        "id": "user-456",
        "email": "bob@example.com",
        "firstName": "Bob",
        "lastName": "Johnson",
        "phone": "987-654-3210",
        "createdAt": "2023-02-20T14:00:00Z"
    }
]

# Data for billing.json
billing_data = [
    {
        "transaction_id": "txn-abc",
        "user_email": "alice@example.com",
        "amount": 99.99,
        "currency": "USD",
        "timestamp": "2023-03-10T11:00:00Z"
    },
    {
        "transaction_id": "txn-def",
        "user_email": "bob@example.com",
        "amount": 49.50,
        "currency": "USD",
        "timestamp": "2023-03-12T18:45:00Z"
    }
]

# Data for marketing.json
marketing_data = [
    {
        "campaign_id": "camp-xyz",
        "recipient_email": "alice@example.com",
        "status": "sent",
        "opened_at": "2023-04-01T09:00:00Z"
    },
    {
        "campaign_id": "camp-uvw",
        "recipient_email": "bob@example.com",
        "status": "clicked",
        "opened_at": "2023-04-05T16:20:00Z"
    }
]

# Write the files
with open('crm.json', 'w') as f:
    json.dump(crm_data, f, indent=4)

with open('billing.json', 'w') as f:
    json.dump(billing_data, f, indent=4)

with open('marketing.json', 'w') as f:
    json.dump(marketing_data, f, indent=4)

print("Mock data files created successfully.")