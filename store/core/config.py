from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseException):
    PROJECT_NAME: str = 'Store API'
    ROOT_PATH: str = "/"

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
