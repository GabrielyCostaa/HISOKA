from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DATABASE_URL: str
    TOKEN_LIFE_MINUTES: int
    TOKEN_ALGORITHM: str
    TOKEN_ASSINATURE_KEY: str
    ORIGINS: list[str]
    API_PORT: int
