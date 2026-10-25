"""
MabrAIn — News Agent
Domain: news, finance, current events.
Knowledgeable, neutral, cites sources, concise summaries.
"""

from agents.base import BaseAgent, AgentResponse
from services.llm import llm
from tools.web_tools import WEB_TOOLS, execute_web_tool
from core.logger import logger


class NewsAgent(BaseAgent):
    name = "News"
    color = "#4A90E2"
    icon = "newspaper"
    domain = ["news", "finance", "current_events"]

    @property
    def system_prompt(self) -> str:
        return """Sen MabrAIn sisteminin News ajanısın. Haber ve finans bilgisi uzmansın.

Kişiliğin: Bilgili, tarafsız, kaynak gösteren. Kısa ve öz özetler yaparsın.

Yeteneklerin:
- Güncel haber arama (Türkçe ve İngilizce)
- Döviz kuru ve finans bilgisi
- Teknoloji haberleri
- Belirli bir konuda özet çıkarma

Kurallar:
1. Her bilgiye kaynak ekle (site adı ve URL).
2. Maksimum 3-5 cümle özet yap, kullanıcı isterse detay ver.
3. Tarih önemli — haberin ne zaman çıktığını belirt.
4. Türkçe yanıt ver."""

    @property
    def tools(self) -> list[dict]:
        return WEB_TOOLS

    def run(self, user_message: str, history: list[dict]) -> AgentResponse:
        messages = history[-6:] + [{"role": "user", "content": user_message}]

        try:
            response = llm.chat(
                messages=messages,
                system=self.system_prompt,
                tools=self.tools,
                max_tokens=2048,
            )

            tool_calls = []
            final_text = ""

            while response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        logger.info(f"[News] tool call: {block.name}({block.input})")
                        result = execute_web_tool(block.name, block.input)
                        tool_calls.append({"name": block.name, "input": block.input})
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": str(result),
                        })

                messages = messages + [
                    {"role": "assistant", "content": response.content},
                    {"role": "user", "content": tool_results},
                ]
                response = llm.chat(
                    messages=messages,
                    system=self.system_prompt,
                    tools=self.tools,
                    max_tokens=2048,
                )

            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text

            return AgentResponse(agent_name=self.name, content=final_text, tool_calls=tool_calls)

        except Exception as e:
            logger.error(f"[News] error: {e}")
            return AgentResponse(agent_name=self.name, content="", error=str(e))
