
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "smartgaon.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS village_reports (
                id TEXT PRIMARY KEY,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT NOT NULL,
                report_method TEXT NOT NULL,
                map_location TEXT,
                photo_name TEXT,
                photo_bytes BLOB,
                submitted_at TEXT NOT NULL
            )
        """)


def save_report(report):
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO village_reports (
                id, category, description, location,
                report_method, map_location, photo_name,
                photo_bytes, submitted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            report["id"],
            report["category"],
            report["description"],
            report["location"],
            report["report_method"],
            report["map_location"],
            report["photo_name"],
            report["photo_bytes"],
            report["submitted_at"]
        ))


def get_all_reports():
    with get_connection() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            "SELECT * FROM village_reports ORDER BY submitted_at DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def delete_report(report_id):
    with get_connection() as connection:
        connection.execute(
            "DELETE FROM village_reports WHERE id = ?",
            (report_id,)
        )
