# Storage Microservice

[PLEASE READ THE ATTACHED INSTRUCTIONS TXT FILE FOR DOWNLOAD AND STARTUP INSTRUCTIONS] This is a python-based microservice used for storing events and data from main program and microservice implementations in a shared suite of group products.
---

## Features

- **Multi-tenancy isolation**: Client records are stored seperately and accessed through client specific API keys.
- **Crash reliability**: Generated data is stored and survives container restarts.
- **Schema validation**: Incoming data packets get validated against Pydantic models.

---

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/v1/storage` | Stores a data/metadata payload and returns a unique UID. |
| `GET` | `/api/v1/storage/{id}` | Retrieves a record by ID |
| `DELETE` | `/api/v1/storage/{id}` | Removes a client record. |

---

## Authentication

All requests require the `X-API-Key` header. The following keys are used for testing and should be changed or deactivated for live system tests:

- `key-simplirecon-secret-123` (Client ID: `SimpliRecon`)
- `key-webapp-secret-456` (Client ID: `WebAppClient`)
- `key-mobile-secret-789` (Client ID: `MobileAppClient`)

---

## Running with Docker

1. Build and start the container:
   ```bash
   docker-compose up --build -d
   ```

2. Verify that the container is running:
   ```bash
   docker ps
   ```

3. Open the interactive GUI in any browser:
   ```text
   http://localhost:5001/docs
   ```

---

## Example Requests

### Create a record

```bash
curl -X POST "http://localhost:5001/api/v1/storage" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: key-simplirecon-secret-123" \
  -d '{
        "data": {"packets": 142, "mode": "Monitor"},
        "metadata": {"source": "SimpliRecon"}
      }'
```

Example response:

```json
{
  "id": "c301e05a-5807-40b5-90f1-435520a03003"
}
```

### Fetch a record

```bash
curl -X GET "http://localhost:5001/api/v1/storage/c301e05a-5807-40b5-90f1-435520a03003" \
  -H "X-API-Key: key-simplirecon-secret-123"
```
