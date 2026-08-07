# main.py
# CS 361 - Summer 2026
# Daniel Magann
# 8/6/2026
# Sources:
# FastAPI documentation: https://fastapi.tiangolo.com/
# SQLite documentation: https://www.sqlite.org/docs.html
# Python UUID module: https://docs.python.org/3/library/uuid.html
# Python JSON module: https://docs.python.org/3/library/json.html
# Description:  A FastAPI application for storing and retrieving records for use alongside a suite
# of microservices and main programs.

import json
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, status

from app.database import get_db, init_db
from app.models import RecordResponse, StoreDataRequest, StoreDataResponse

app = FastAPI(
    title="Unified Storage Microservice",
    description="A lightweight service for persisting application data with tenant-aware access control.",
)

# Predefined client credentials, Hard coded credentials omitted from Github code
VALID_CLIENT_KEYS = {
    "################": "##############",
    "#################": "##############",
    "#################": "###############",
}


@app.on_event("startup")
def startup_event() -> None:
    """
    Initialize SQL schema
    """
    init_db()


def authenticate_client(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """
    Validate the incoming API key and return the client identifier.
    """
    client_id = VALID_CLIENT_KEYS.get(x_api_key)
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized: Invalid API key",
        )
    return client_id


@app.post("/api/v1/storage", response_model=StoreDataResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    payload: StoreDataRequest,
    client_id: str = Depends(authenticate_client),
) -> StoreDataResponse:
    """
    Create a new record and return generated identifier.
    """
    record_id = str(uuid.uuid4())
    data_str = json.dumps(payload.data)
    meta_str = json.dumps(payload.metadata) if payload.metadata else json.dumps({})

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO storage_records (id, client_id, data, metadata) VALUES (?, ?, ?, ?)
            """,
            (record_id, client_id, data_str, meta_str),
        )
        conn.commit()

    return {"id": record_id}


@app.get("/api/v1/storage/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: str,
    client_id: str = Depends(authenticate_client),
) -> RecordResponse:
    """
    Get a record by ID
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, client_id, data, metadata FROM storage_records WHERE id = ? AND client_id = ?",
            (record_id, client_id),
        )
        row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found or access denied.",
        )

    return {
        "id": row["id"],
        "client_id": row["client_id"],
        "data": json.loads(row["data"]),
        "metadata": json.loads(row["metadata"]),
    }


@app.delete("/api/v1/storage/{record_id}", status_code=status.HTTP_200_OK)
def delete_record(
    record_id: str,
    client_id: str = Depends(authenticate_client),
) -> dict[str, str]:
    """
    Delete Record by ID
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM storage_records WHERE id = ? AND client_id = ?",
            (record_id, client_id),
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Record not found or access denied.",
            )

    return {"message": f"Record {record_id} successfully deleted."}
