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
    media_folder: str

    reauth_path: str

    recaptcha_site_key: str
    recaptcha_secret_key: str


settings = Settings()
