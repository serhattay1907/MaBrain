"""
MabrAIn — Core Configuration
Loads settings from .env. All other modules import from here.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # LLM
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    primary_model: str = "claude-sonnet-4-20250514"

    # Token budget (daily cap — safety net against runaway loops)
    daily_token_budget: int = Field(100_000, env="DAILY_TOKEN_BUDGET")

    # Server
    backend_host: str = "127.0.0.1"
    backend_port: int = 8765

    # Paths (relative to backend/)
    data_dir: str = "data"
    log_dir: str = "logs"
    whisper_model_path: str = Field("", env="WHISPER_MODEL_PATH")
    piper_model_path: str = Field("", env="PIPER_MODEL_PATH")

    # Conscience agent — whitelisted folders (comma-separated, set by user at onboarding)
    allowed_folders: str = Field("", env="ALLOWED_FOLDERS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_allowed_folders(self) -> list[str]:
        if not self.allowed_folders:
            return []
        return [f.strip() for f in self.allowed_folders.split(",") if f.strip()]


# Singleton — import this everywhere
settings = Settings()
