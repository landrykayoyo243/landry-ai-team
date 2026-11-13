from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "landry-ai-team"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./landry_ai_team.db"
    secret_key: str = "change-me-in-production"

    telegram_manager_bot_token: str = ""
    telegram_coder_bot_token: str = ""
    telegram_reviewer_bot_token: str = ""

    allowed_telegram_users: str = ""
    github_token: str = ""
    github_repo: str = "landrykayoyo243/landry-ai-team"

    openai_api_key: str = ""
    anthropic_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    anthropic_model: str = "claude-3-5-sonnet-20241022"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
