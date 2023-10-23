from os.path import isfile

from pydantic_settings import BaseSettings


ENV_DEVELOPMENT = ".dev.env"
ENV_PRODUCTION = ".env"


class Settings(BaseSettings):
    class Config:
        env_file = ENV_DEVELOPMENT if isfile(ENV_DEVELOPMENT) else ENV_PRODUCTION

    project_name: str

    secret_key: str

    admin_login: str
    admin_password: str

    database_path: str

    template_folder: str
    static_folder: str

    reauth_path: str


settings = Settings()
