"""
MabrAIn — Daily Token Budget
Counts tokens used today. Raises BudgetExceededError when the daily limit is hit.
This is a safety net against runaway loops or bugs burning API credits overnight.
"""

import json
from datetime import date
from pathlib import Path

from core.config import settings
from core.logger import logger


class BudgetExceededError(Exception):
    """Raised when the daily token budget is exhausted."""


class TokenBudget:
    def __init__(self):
        self._data_dir = Path(settings.data_dir)
        self._data_dir.mkdir(parents=True, exist_ok=True)
        self._file = self._data_dir / "token_budget.json"
        self._state = self._load()

    def _load(self) -> dict:
        today = str(date.today())
        if self._file.exists():
            data = json.loads(self._file.read_text())
            if data.get("date") == today:
                return data
        return {"date": today, "used": 0}

    def _save(self):
        self._file.write_text(json.dumps(self._state))

    def consume(self, tokens: int):
        today = str(date.today())
        if self._state["date"] != today:
            self._state = {"date": today, "used": 0}

        self._state["used"] += tokens
        self._save()
        logger.debug(f"Token budget: {self._state['used']} / {settings.daily_token_budget} used today")

        if self._state["used"] > settings.daily_token_budget:
            raise BudgetExceededError(
                f"Daily token budget ({settings.daily_token_budget:,}) exceeded. "
                "Restart tomorrow or raise DAILY_TOKEN_BUDGET in .env."
            )

    @property
    def used_today(self) -> int:
        self._state = self._load()
        return self._state["used"]

    @property
    def remaining(self) -> int:
        return max(0, settings.daily_token_budget - self.used_today)


# Singleton
budget = TokenBudget()
