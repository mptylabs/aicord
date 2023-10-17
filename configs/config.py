from pydantic_settings import BaseSettings, SettingsConfigDict

from typing import List


class DiscordSettings(BaseSettings):
    token: str
    owner_guild_ids: List[int]
    owner_ids: List[int]


class Settings(BaseSettings):
    discord: DiscordSettings
    openai_token: str

    model_config = SettingsConfigDict(env_nested_delimiter='__',
                                      env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')


settings = Settings()
