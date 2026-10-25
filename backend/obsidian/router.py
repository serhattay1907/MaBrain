"""
MabrAIn — Obsidian Orchestrator: Intent Router
Asks Claude to classify the user's intent into an agent domain.
Target accuracy: >=85% (measured by tests/router_eval.json).
"""

from services.llm import llm
from core.logger import logger

DOMAIN_TO_AGENT = {
    "file_management": "conscience",
    "task_organization": "conscience",
    "reminder": "daily",
    "schedule": "daily",
    "daily_routine": "daily",
    "news": "news",
    "finance": "news",
    "current_events": "news",
    "unknown": None,
}

CLASSIFIER_SYSTEM = """Sen bir niyet sınıflandırıcısın. Kullanıcının mesajını analiz et ve hangi domain'e ait olduğunu belirle.

Mevcut domain'ler:
- file_management: dosya/klasör işlemleri (listeleme, taşıma, arama, yeniden adlandırma)
- task_organization: görev listesi, not alma, proje düzenleme
- reminder: hatırlatma oluşturma, silme, listeleme
- schedule: takvim, ders programı, randevu
- daily_routine: sabah/akşam rutini, günlük plan
- news: haber, güncel olaylar, manşetler
- finance: döviz kuru, borsa, kripto, ekonomi
- current_events: spor, politika, teknoloji haberleri
- unknown: yukarıdakilerden hiçbiri

SADECE şu JSON formatında yanıt ver, başka hiçbir şey yazma:
{"domain": "<domain_adı>", "confidence": 0.0-1.0}"""


def classify_intent(user_message: str, history: list[dict] | None = None) -> tuple[str, str]:
    """
    Returns (agent_key, domain).
    agent_key is one of: 'conscience', 'daily', 'news', or None for unknown.
    """
    messages = [{"role": "user", "content": user_message}]

    try:
        response = llm.chat(
            messages=messages,
            system=CLASSIFIER_SYSTEM,
            max_tokens=64,
        )
        text = ""
        for block in response.content:
            if hasattr(block, "text"):
                text += block.text

        import json
        result = json.loads(text.strip())
        domain = result.get("domain", "unknown")
        confidence = result.get("confidence", 0.0)

        logger.info(f"[Router] domain='{domain}' confidence={confidence:.2f} | '{user_message[:60]}'")

        agent_key = DOMAIN_TO_AGENT.get(domain, None)
        return agent_key, domain

    except Exception as e:
        logger.error(f"[Router] classification failed: {e}")
        return None, "unknown"
