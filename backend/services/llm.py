"""
MabrAIn — LLM Service (Abstraction Layer)
All agents call this module. Swapping providers = edit only this file.
"""

from anthropic import Anthropic
from core.config import settings
from core.budget import budget, BudgetExceededError
from core.logger import logger


class LLMService:
    def __init__(self):
        self._client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.primary_model

    def chat(
        self,
        messages: list[dict],
        system: str = "",
        tools: list[dict] | None = None,
        max_tokens: int = 1024,
    ) -> dict:
        """
        Single-turn chat. Returns the full Anthropic Message object as a dict.
        Tracks token usage against the daily budget.
        """
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools

        logger.debug(f"LLM request — model={self.model}, messages={len(messages)}")
        response = self._client.messages.create(**kwargs)

        # Track usage
        usage = response.usage
        total = usage.input_tokens + usage.output_tokens
        budget.consume(total)
        logger.debug(f"LLM response — in={usage.input_tokens} out={usage.output_tokens}")

        return response

    def stream_chat(
        self,
        messages: list[dict],
        system: str = "",
        max_tokens: int = 1024,
    ):
        """
        Streaming chat. Yields text delta strings as they arrive.
        Token tracking happens on stream completion.
        """
        kwargs = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system

        with self._client.messages.stream(**kwargs) as stream:
            for text in stream.text_stream:
                yield text

            # Count tokens after stream ends
            final = stream.get_final_message()
            usage = final.usage
            total = usage.input_tokens + usage.output_tokens
            budget.consume(total)


# Singleton
llm = LLMService()
