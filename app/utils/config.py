import pydantic

class Settings(pydantic.BaseSettings):
    TRACKING_CODE_PREFIX="PACKAGE"
    TRACKING_CODE_PADDING=5

