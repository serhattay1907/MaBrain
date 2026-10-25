from agents.conscience import ConscienceAgent
from agents.daily import DailyAgent
from agents.news import NewsAgent

AGENT_REGISTRY = {
    "conscience": ConscienceAgent(),
    "daily": DailyAgent(),
    "news": NewsAgent(),
}
