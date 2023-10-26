from os.path import isfile

from pydantic_settings import BaseSettings


ENV_DEVELOPMENT = ".dev.env"
ENV_PRODUCTION = ".env"


class Settings(BaseSettings):
    class Config:
        env_file = ENV_DEVELOPMENT if isfile(ENV_DEVELOPMENT) else ENV_PRODUCTION

    project_name: str

    secret_key: str

    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_password: str
    postgres_database: str

    admin_login: str
    admin_password: str

    rules_link: str
    news_link: str
    offer_link: str
    stats_link: str
    chat_link: str
    about_link: str

    template_folder: str
    static_folder: str
    media_folder: str

    recaptcha_site_key: str
    recaptcha_secret_key: str

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@" \
               f"{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"


settings = Settings()
