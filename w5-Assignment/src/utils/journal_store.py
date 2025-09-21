import os
import sqlite3
from typing import Optional, List, Dict, Any


DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "journal.db")

# -----------------------------
# Ensure the data directory exists.
# -----------------------------
def _ensure_dir():
    os.makedirs(DB_DIR, exist_ok=True)

# -----------------------------
# Create the SQLite DB and entries table if missing; apply best-effort migrations.
# -----------------------------
def init_db() -> None:
    """Create the journal database and table if they don't exist."""
    _ensure_dir()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                date TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                sentiment TEXT,
                sentiment_score REAL,
                reflection TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()

        # -----------------------------
        # Simple migration if existing table lacks 'reflection'
        # Simple migrations (best effort)
        # -----------------------------
        for col_def in [
            ("reflection", "TEXT"),
            ("sentiment_score", "REAL"),
        ]:
            try:
                conn.execute(f"ALTER TABLE entries ADD COLUMN {col_def[0]} {col_def[1]}")
            except sqlite3.OperationalError:
                # Column already exists; ignore
                pass


def upsert_entry(
    date_str: str,
    content: str,
    sentiment: Optional[str] = None,
    reflection: Optional[str] = None,
    sentiment_score: Optional[float] = None,
) -> None:
    """Insert or update a journal entry for a specific date (YYYY-MM-DD)."""
    _ensure_dir()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO entries(date, content, sentiment, reflection, sentiment_score)
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                content = excluded.content,
                sentiment = excluded.sentiment,
                reflection = excluded.reflection,
                sentiment_score = excluded.sentiment_score
            """,
            (date_str, content, sentiment, reflection, sentiment_score),
        )
        conn.commit()

# -----------------------------
# Fetch a single entry by date (YYYY-MM-DD) or return None.
# -----------------------------
def get_entry_by_date(date_str: str) -> Optional[Dict[str, Any]]:
    """Fetch an entry by date. Returns dict or None."""
    if not os.path.exists(DB_PATH):
        return None
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT date, content, sentiment, sentiment_score, reflection, created_at FROM entries WHERE date = ?",
            (date_str,),
        )
        row = cur.fetchone()
        return dict(row) if row else None

# -----------------------------
# List up to 'limit' recent entries, newest first.
# -----------------------------
def list_entries(limit: int = 10) -> List[Dict[str, Any]]:
    """List recent entries, newest first."""
    if not os.path.exists(DB_PATH):
        return []
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT date, content, sentiment, sentiment_score, reflection, created_at FROM entries ORDER BY date DESC LIMIT ?",
            (limit,),
        )
        return [dict(r) for r in cur.fetchall()]

# -----------------------------
# Return a list of {date, sentiment, sentiment_score} for the last N days.
# -----------------------------
def sentiment_trend(days: int = 14) -> List[Dict[str, Any]]:
    """Return date and sentiment_score for last N days (if present)."""
    if not os.path.exists(DB_PATH):
        return []
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            """
            SELECT date, sentiment, sentiment_score
            FROM entries
            WHERE date >= date('now', ?)
            ORDER BY date ASC
            """,
            (f"-{days} day",),
        )
        return [dict(r) for r in cur.fetchall()]
