"""
MabrAIn — Phase 1 CLI
Simple command-line interface for testing agents without a UI.
Usage: python cli.py
"""

from dotenv import load_dotenv
load_dotenv()

from obsidian.router import classify_intent
from obsidian.memory import memory
from agents import AGENT_REGISTRY
from core.budget import budget
from core.logger import logger


def main():
    print("=" * 50)
    print("MabrAIn CLI — Faz 1 Test Arayüzü")
    print("Çıkmak için: 'q' veya Ctrl+C")
    print("=" * 50)
    print()

    while True:
        try:
            user_input = input("Sen: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGüle güle!")
            break

        if not user_input or user_input.lower() in ("q", "quit", "çıkış"):
            print("Güle güle!")
            break

        # Route intent
        agent_key, domain = classify_intent(user_input)
        print(f"[Router → {agent_key or 'bilinmiyor'} | domain: {domain}]")

        memory.add("user", user_input)

        if agent_key is None or agent_key not in AGENT_REGISTRY:
            response_text = "Bu konuda yardımcı olacak bir ajanım yok. Dosya işlemleri, hatırlatmalar veya haber için sorabilirsin."
            print(f"MabrAIn: {response_text}\n")
            memory.add("assistant", response_text)
            continue

        agent = AGENT_REGISTRY[agent_key]
        result = agent.run(user_input, memory.get_recent(10))

        if result.error:
            response_text = f"Üzgünüm, bir hata oluştu: {result.error}"
        else:
            response_text = result.content

        print(f"{result.agent_name}: {response_text}")
        print(f"[Bütçe: {budget.used_today:,} / {budget.remaining + budget.used_today:,} token kullanıldı]\n")

        memory.add("assistant", response_text, agent=agent_key)


if __name__ == "__main__":
    main()
