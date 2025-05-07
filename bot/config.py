from dataclasses import dataclass
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    token: str = Field(..., env="BOT_TOKEN")
    admin_ids: List[int] = Field(default_factory=list, env="ADMIN_IDS")
    daily_bonus: int = Field(default=100, env="DAILY_BONUS")
    tap_cooldown_seconds: int = Field(default=5, env="TAP_COOLDOWN_SECONDS")
    base_tap_reward: int = Field(default=1, env="BASE_TAP_REWARD")


class DatabaseSettings(BaseSettings):
    host: str = Field(default="localhost", env="POSTGRES_HOST")
    port: int = Field(default=5432, env="POSTGRES_PORT")
    user: str = Field(default="postgres", env="POSTGRES_USER")
    password: str = Field(default="postgres", env="POSTGRES_PASSWORD")
    database: str = Field(default="crapcoin", env="POSTGRES_DB")

    @property
    def url(self) -> str:
        """Получить URL для подключения к базе данных."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")


@dataclass
class Config:
    bot: BotSettings
    db: DatabaseSettings
    redis: RedisSettings


def load_config() -> Config:
    bot_settings = BotSettings()
    db_settings = DatabaseSettings()
    redis_settings = RedisSettings()
    
    return Config(
        bot=bot_settings,
        db=db_settings,
        redis=redis_settings
    )
