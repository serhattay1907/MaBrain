"""
MabrAIn — Base Agent Template
Every agent (Conscience, Daily, News) inherits from BaseAgent.
Fill in: system_prompt, tools, color, icon, name.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AgentResponse:
    agent_name: str
    content: str
    tool_calls: list[dict] = field(default_factory=list)
    error: str | None = None


class BaseAgent(ABC):
    # --- Override these in each agent ---
    name: str = "BaseAgent"
    color: str = "#FFFFFF"
    icon: str = "bot"
    domain: list[str] = []

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """The agent's personality and rules."""
        ...

    @property
    def tools(self) -> list[dict]:
        """Tool definitions in Anthropic format. Override to add tools."""
        return []

    @abstractmethod
    def run(self, user_message: str, history: list[dict]) -> AgentResponse:
        """
        Execute the agent for a single user turn.
        `history` is the recent conversation (last N messages).
        Returns an AgentResponse.
        """
        ...

    def __repr__(self):
        return f"<Agent: {self.name} | domains={self.domain}>"
