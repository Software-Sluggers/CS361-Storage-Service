 CS361 Storage Microservice

A basic Python FastAPI service used to persist JSON records and metadata across group microservices.

## Setup & Running with Docker

1. Build and run the container:
   ```bash
   docker-compose up --build -d
Check running status:

(Bash)
docker ps
View FastAPI interactive docs:
Open http://localhost:5001/docs in your browser.

API Authentication
All requests require an X-API-Key header:

key-simplirecon-secret-123 (SimpliRecon)

key-webapp-secret-456 (WebAppClient)

key-mobile-secret-789 (MobileAppClient)

API Endpoints
POST /api/v1/storage - Store a new record (returns UID)

GET /api/v1/storage/{id} - Fetch record by ID

DELETE /api/v1/storage/{id} - Delete record by ID

Example Requests
Create Record:

Bash
curl -X POST "http://localhost:5001/api/v1/storage" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: key-simplirecon-secret-123" \
  -d '{
        "data": {"packets": 142, "mode": "Monitor"},
        "metadata": {"source": "SimpliRecon"}
      }'
Get Record:

Bash
curl -X GET "http://localhost:5001/api/v1/storage/<YOUR_RECORD_ID>" \
  -H "X-API-Key: key-simplirecon-secret-123"

---
