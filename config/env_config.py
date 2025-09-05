from pydantic_settings import BaseSettings

class EnvConfig(BaseSettings):
    comet_ml_api: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

envconfig = EnvConfig()