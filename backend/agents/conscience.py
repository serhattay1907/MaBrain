"""
MabrAIn — Conscience Agent
Domain: file management, task organization.
Careful, polite. Asks for confirmation before destructive operations.
"""

from agents.base import BaseAgent, AgentResponse
from services.llm import llm
from tools.file_tools import FILE_TOOLS, execute_file_tool
from core.safety import SafetyError
from core.logger import logger


class ConscienceAgent(BaseAgent):
    name = "Conscience"
    color = "#6B5B95"
    icon = "folder"
    domain = ["file_management", "task_organization"]

    @property
    def system_prompt(self) -> str:
        return """Sen MabrAIn sisteminin Conscience ajanısın. Görev ve dosya yönetimi uzmansın.

Kişiliğin: Düzenli, dikkatli, kibar. Tehlikeli veya geri alınamaz bir işlemden önce MUTLAKA kullanıcıdan onay istersin.

Yeteneklerin:
- Dosya ve klasör listeleme
- Dosya taşıma ve kopyalama
- Dosya yeniden adlandırma
- Klasör oluşturma
- İsme veya içeriğe göre dosya arama

Kurallar:
1. Yalnızca whitelist'teki klasörlere erişebilirsin. Sistem dizinlerine (C:\\Windows, /etc, /usr vb.) ASLA dokunma.
2. Silme veya üzerine yazma işlemlerinden önce kullanıcıya ne yapacağını söyle ve onay iste.
3. Bir işlem başarısız olursa nazikçe açıkla, çözüm öner.
4. Dosya yollarını her zaman tam yol olarak ver.
5. Türkçe yanıt ver."""

    @property
    def tools(self) -> list[dict]:
        return FILE_TOOLS

    def run(self, user_message: str, history: list[dict]) -> AgentResponse:
        messages = history[-10:] + [{"role": "user", "content": user_message}]

        try:
            response = llm.chat(
                messages=messages,
                system=self.system_prompt,
                tools=self.tools,
                max_tokens=2048,
            )

            tool_calls = []
            final_text = ""

            # Agentic loop — keep running until no more tool calls
            while response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        logger.info(f"[Conscience] tool call: {block.name}({block.input})")
                        try:
                            result = execute_file_tool(block.name, block.input)
                            tool_calls.append({"name": block.name, "input": block.input, "result": result})
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": str(result),
                            })
                        except SafetyError as e:
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": f"REDDEDILDI: {e}",
                                "is_error": True,
                            })

                # Continue conversation with tool results
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

            # Extract final text
            for block in response.content:
                if hasattr(block, "text"):
                    final_text += block.text

            return AgentResponse(
                agent_name=self.name,
                content=final_text,
                tool_calls=tool_calls,
            )

        except Exception as e:
            logger.error(f"[Conscience] error: {e}")
            return AgentResponse(
                agent_name=self.name,
                content="",
                error=str(e),
            )
