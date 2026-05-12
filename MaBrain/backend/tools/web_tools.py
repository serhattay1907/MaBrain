"""
MabrAIn — Web Tools (News Agent)
DuckDuckGo search via httpx (no API key required for basic usage).
"""

import httpx
from core.logger import logger

WEB_TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for news or information using DuckDuckGo.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query string."},
                "language": {"type": "string", "default": "tr-TR", "description": "Language code."},
            },
            "required": ["query"],
        },
    },
]


def search_web(query: str, language: str = "tr-TR") -> str:
    """
    Lightweight DuckDuckGo instant-answer search.
    For Phase 3, replace with DuckDuckGo HTML scraping or Brave Search API.
    """
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_redirect": "1",
            "no_html": "1",
            "skip_disambig": "1",
        }
        r = httpx.get(url, params=params, timeout=10)
        data = r.json()
        abstract = data.get("AbstractText", "")
        source = data.get("AbstractSource", "")
        if abstract:
            return f"{abstract}\n\nKaynak: {source}"
        # Fallback: related topics
        topics = data.get("RelatedTopics", [])[:5]
        lines = [t.get("Text", "") for t in topics if isinstance(t, dict)]
        if lines:
            return "\n".join(lines)
        return f"'{query}' için sonuç bulunamadı. (Not: Faz 3'te gelişmiş arama eklenecek)"
    except Exception as e:
        logger.error(f"[web_search] error: {e}")
        return f"Arama başarısız: {e}"


def execute_web_tool(name: str, params: dict) -> str:
    dispatch = {"search_web": search_web}
    if name not in dispatch:
        return f"Bilinmeyen tool: {name}"
    return dispatch[name](**params)
