"""
MabrAIn — Daily Agent
Domain: reminders, schedule, daily routine.
Warm, motivating, morning/evening check-ins.
"""

from agents.base import BaseAgent, AgentResponse
from services.llm import llm
from tools.reminder_tools import REMINDER_TOOLS, execute_reminder_tool
from core.logger import logger


class DailyAgent(BaseAgent):
    name = "Daily"
    color = "#FFB347"
    icon = "sun"
    domain = ["reminder", "schedule", "daily_routine"]

    @property
    def system_prompt(self) -> str:
        return """Sen MabrAIn sisteminin Daily ajanısın. Hatırlatma ve günlük rutin yönetimi uzmansın.

Kişiliğin: Sıcak, motive edici, hatırlatıcı. Sabah ve akşam selaması yaparsın. Kullanıcının günlük rutinini bilirsin.

Yeteneklerin:
- Hatırlatma oluşturma (tarih/saat ile)
- Hatırlatmaları listeleme (bugün, bu hafta, tümü)
- Hatırlatma silme ve güncelleme
- Yaklaşan görevleri özetleme

Kurallar:
1. Tarih/saat belirtilmemişse mutlaka sor.
2. Kullanıcının ismini biliyorsan kullan.
3. Türkçe yanıt ver.
4. Kısa ve nazik ol."""

    @property
    def tools(self) -> list[dict]:
        return REMINDER_TOOLS

    def run(self, user_message: str, history: list[dict]) -> AgentResponse:
        messages = history[-10:] + [{"role": "user", "content": user_message}]

        try:
            response = llm.chat(
                messages=messages,
                system=self.system_prompt,
                tools=self.tools,
                max_tokens=1024,
            )

            tool_calls = []
            final_text = ""

            while response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        logger.info(f"[Daily] tool call: {block.name}({block.input})")
                        result = execute_reminder_tool(block.name, block.input)
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
                    max_tokens=1024,
                )

            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text

            return AgentResponse(agent_name=self.name, content=final_text, tool_calls=tool_calls)

        except Exception as e:
            logger.error(f"[Daily] error: {e}")
            return AgentResponse(agent_name=self.name, content="", error=str(e))
