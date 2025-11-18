from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TRACKING_CODE_PREFIX: str = "PACKAGE"
    TRACKING_CODE_PADDING: int = 5


    # model_config = SettingsConfigDict(
    #     env_file=".env",
    #     env_file_encoding="utf-8",
    # )
settings = Settings()

API_KEY = "abc"