from fastapi import Request

from settings import settings


SESSION_KEY: str = "superuser"
AUTHENTICATED: bool = True


class AdminAuth:
    @staticmethod
    def check_credentials(login: str, password: str) -> bool:
        return login == settings.admin_login and password == settings.admin_password

    @staticmethod
    def authenticate(request: Request) -> None:
        request.session[SESSION_KEY] = AUTHENTICATED

    @staticmethod
    def is_authenticated(request: Request) -> bool:
        return request.session.get(SESSION_KEY, False)

    @staticmethod
    def deauthenticate(request: Request) -> None:
        request.session.pop(SESSION_KEY)
