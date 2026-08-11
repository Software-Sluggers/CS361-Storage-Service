# main.py
# CS 361 - Summer 2026
# Daniel Magann
# 8/6/2026
# Sources:
# FastAPI Docs: https://fastapi.tiangolo.com/
# SQLite Docs: https://www.sqlite.org/docs.html
# Pydantic Docs: https://docs.pydantic.dev/

import json
import os
import sqlite3
import uuid
from typing import Any, Dict, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Storage Microservice")

DB_PATH = os.getenv("DATABASE_PATH", "/app/data/storage.db")

# API Keys, client names
VALID_CLIENT_KEYS = {
    "key-simplirecon-secret-123": "SimpliRecon",
    "key-webapp-secret-456": "WebAppClient",
    "key-mobile-secret-789": "MobileAppClient",
}


# Helper functions

def get_db() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS storage_records (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                data TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_client_record
            ON storage_records(client_id, id)
            """
        )
        conn.commit()


@app.on_event("startup")
def startup_event():
    init_db()


# Authentication

def authenticate_client(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    client_id = VALID_CLIENT_KEYS.get(x_api_key)
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return client_id


# Pydantic

class StoreDataRequest(BaseModel):
    data: Dict[str, Any] = Field(..., description="Application data payload")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional metadata",
    )


# API Routes

@app.post("/api/v1/storage", status_code=201)
def create_record(
    payload: StoreDataRequest,
    client_id: str = Depends(authenticate_client),
):
    record_id = str(uuid.uuid4())
    data_str = json.dumps(payload.data)
    meta_str = json.dumps(payload.metadata or {})

    with get_db() as conn:
        conn.execute(
            "INSERT INTO storage_records (id, client_id, data, metadata) VALUES (?, ?, ?, ?)",
            (record_id, client_id, data_str, meta_str),
        )
        conn.commit()

    return {"id": record_id}


@app.get("/api/v1/storage/{record_id}")
def get_record(
    record_id: str,
    client_id: str = Depends(authenticate_client),
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, client_id, data, metadata FROM storage_records WHERE id = ? AND client_id = ?",
            (record_id, client_id),
        )
        row = cursor.fetchone()

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Record not found",
        )

    return {
        "id": row["id"],
        "client_id": row["client_id"],
        "data": json.loads(row["data"]),
        "metadata": json.loads(row["metadata"]),
    }


@app.delete("/api/v1/storage/{record_id}")
def delete_record(
    record_id: str,
    client_id: str = Depends(authenticate_client),
):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM storage_records WHERE id = ? AND client_id = ?",
            (record_id, client_id),
        )
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Record not found",
            )

    return {"message": f"Record {record_id} deleted."}
