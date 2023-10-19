from os.path import isfile

from pydantic_settings import BaseSettings


ENV_DEVELOPMENT = ".dev.env"
ENV_PRODUCTION = ".env"


class Settings(BaseSettings):
    class Config:
        env_file = ENV_DEVELOPMENT if isfile(ENV_DEVELOPMENT) else ENV_PRODUCTION

    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_database: str

    admin_login: str
    admin_password: str

    template_folder: str


settings = Settings()
