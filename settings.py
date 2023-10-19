from os.path import isfile

from pydantic_settings import BaseSettings


ENV_DEVELOPMENT = ".dev.env"
ENV_PRODUCTION = ".env"


class Settings(BaseSettings):
    class Config:
        env_file = ENV_DEVELOPMENT if isfile(ENV_DEVELOPMENT) else ENV_PRODUCTION

    project_name: str

    database_path: str

    admin_login: str
    admin_password: str

    template_folder: str
    static_folder: str


settings = Settings()
