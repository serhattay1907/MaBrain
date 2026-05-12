"""
MabrAIn — Phase 0 Hello World
Run this first to verify your Anthropic API key works.
Usage: python hello_world.py
"""

from dotenv import load_dotenv
load_dotenv()

from core.config import settings
from services.llm import llm


def main():
    print("=" * 50)
    print("MabrAIn — Phase 0 Hello World")
    print("=" * 50)
    print(f"Model: {settings.primary_model}")
    print(f"Daily budget: {settings.daily_token_budget:,} tokens")
    print()

    response = llm.chat(
        messages=[{"role": "user", "content": "Merhaba! Sen kimsin? Bir cümlede anlat."}],
        system="Sen MabrAIn sisteminin test ajanısın. Türkçe yanıt ver.",
        max_tokens=100,
    )

    for block in response.content:
        if hasattr(block, "text"):
            print("Claude yanıtı:", block.text)

    print()
    print(f"✅ API bağlantısı başarılı! Kullanılan token: {response.usage.input_tokens + response.usage.output_tokens}")


if __name__ == "__main__":
    main()
