"""
MabrAIn — Reminder Tools (Daily Agent)
Uses SQLite for local, persistent storage.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from core.config import settings

DB_PATH = Path(settings.data_dir) / "reminders.db"


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            due_at TEXT,
            created_at TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


REMINDER_TOOLS = [
    {
        "name": "create_reminder",
        "description": "Create a new reminder.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Reminder text."},
                "due_at": {"type": "string", "description": "ISO datetime string, e.g. '2026-05-15T10:00:00'"},
            },
            "required": ["text"],
        },
    },
    {
        "name": "list_reminders",
        "description": "List reminders. Filter: 'today', 'week', or 'all'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filter": {"type": "string", "enum": ["today", "week", "all"], "default": "all"},
            },
        },
    },
    {
        "name": "delete_reminder",
        "description": "Delete a reminder by its ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reminder_id": {"type": "integer"},
            },
            "required": ["reminder_id"],
        },
    },
]


def create_reminder(text: str, due_at: str | None = None) -> str:
    conn = _get_conn()
    now = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO reminders (text, due_at, created_at) VALUES (?, ?, ?)",
        (text, due_at, now)
    )
    conn.commit()
    conn.close()
    due_str = f" — {due_at}" if due_at else ""
    return f"✅ Hatırlatma eklendi: '{text}'{due_str}"


def list_reminders(filter: str = "all") -> str:
    conn = _get_conn()
    today = datetime.now().date().isoformat()
    if filter == "today":
        rows = conn.execute(
            "SELECT id, text, due_at FROM reminders WHERE done=0 AND due_at LIKE ? ORDER BY due_at",
            (f"{today}%",)
        ).fetchall()
    elif filter == "week":
        rows = conn.execute(
            "SELECT id, text, due_at FROM reminders WHERE done=0 ORDER BY due_at LIMIT 20"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, text, due_at FROM reminders WHERE done=0 ORDER BY due_at"
        ).fetchall()
    conn.close()
    if not rows:
        return "Hatırlatma bulunamadı."
    lines = [f"[{r[0]}] {r[1]}" + (f" — {r[2]}" if r[2] else "") for r in rows]
    return "\n".join(lines)


def delete_reminder(reminder_id: int) -> str:
    conn = _get_conn()
    cursor = conn.execute("DELETE FROM reminders WHERE id=?", (reminder_id,))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return f"ID {reminder_id} bulunamadı."
    return f"✅ Hatırlatma #{reminder_id} silindi."


def execute_reminder_tool(name: str, params: dict) -> str:
    dispatch = {
        "create_reminder": create_reminder,
        "list_reminders": list_reminders,
        "delete_reminder": delete_reminder,
    }
    if name not in dispatch:
        return f"Bilinmeyen tool: {name}"
    return dispatch[name](**params)
