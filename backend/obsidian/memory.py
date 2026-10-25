"""
MabrAIn — Conversation Memory
In-memory (last N messages) + SQLite persistence.
Phase 3 will add vector memory via ChromaDB.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from core.config import settings
from core.logger import logger

DB_PATH = Path(settings.data_dir) / "conversation_history.db"
MAX_IN_MEMORY = 20  # messages kept in RAM for context


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            agent TEXT,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


class ConversationMemory:
    def __init__(self):
        self._buffer: list[dict] = []
        self._load_recent()

    def _load_recent(self):
        try:
            conn = _get_conn()
            rows = conn.execute(
                "SELECT role, content FROM history ORDER BY id DESC LIMIT ?",
                (MAX_IN_MEMORY,)
            ).fetchall()
            conn.close()
            self._buffer = [{"role": r[0], "content": r[1]} for r in reversed(rows)]
        except Exception as e:
            logger.warning(f"[Memory] could not load history: {e}")

    def add(self, role: str, content: str, agent: str | None = None):
        self._buffer.append({"role": role, "content": content})
        if len(self._buffer) > MAX_IN_MEMORY:
            self._buffer.pop(0)

        try:
            conn = _get_conn()
            conn.execute(
                "INSERT INTO history (role, content, agent, timestamp) VALUES (?,?,?,?)",
                (role, content, agent, datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"[Memory] write error: {e}")

    def get_recent(self, n: int = 10) -> list[dict]:
        return self._buffer[-n:]

    def clear(self):
        self._buffer = []


# Singleton
memory = ConversationMemory()
