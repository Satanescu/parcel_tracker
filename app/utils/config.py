from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TRACKING_CODE_PREFIX: str = "PACKAGE"
    TRACKING_CODE_PADDING: int = 5

    # opțional: de unde citește .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
settings = Settings()