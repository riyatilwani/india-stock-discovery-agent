import json
import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path(__file__).resolve().parents[2] / "data" / "app.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS investor_profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age_range TEXT NOT NULL,
                experience TEXT NOT NULL,
                risk_tolerance TEXT NOT NULL,
                horizon_years INTEGER NOT NULL,
                monthly_investment INTEGER NOT NULL,
                emergency_fund_months INTEGER NOT NULL,
                income_stability TEXT NOT NULL,
                max_drawdown_percent INTEGER NOT NULL,
                goals_json TEXT NOT NULL,
                existing_investments TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                company_name TEXT NOT NULL,
                suitability_label TEXT NOT NULL,
                decision TEXT NOT NULL,
                thesis TEXT NOT NULL,
                risks_json TEXT NOT NULL,
                notes TEXT NOT NULL,
                follow_up_date TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def encode_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def decode_json(value: str) -> Any:
    return json.loads(value) if value else None
