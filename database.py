# database.py
# CS 361 - Summer 2026
# Daniel Magann
# 8/6/2026
# Sources:
# FastAPI documentation: https://fastapi.tiangolo.com/
# SQLite documentation: https://www.sqlite.org/docs.html
# Python UUID module: https://docs.python.org/3/library/uuid.html
# Python JSON module: https://docs.python.org/3/library/json.html
# Description: These are the database helper functions for the Storage Service.

import os
import sqlite3 # Brings me back to the database class last quarter

DB_PATH = os.getenv("DATABASE_PATH", "/app/data/storage.db")


def get_db() -> sqlite3.Connection:
    """
    Creates and establishesa SQLite connection
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Creates the storage table and supporting index if they do not already exist.
    """
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