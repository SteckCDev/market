from fastapi import Request


SESSION_KEY: str = "superuser"
AUTHENTICATED: bool = True


class Admin:
    @staticmethod
    def authenticate(request: Request) -> None:
        request.session[SESSION_KEY] = AUTHENTICATED

    @staticmethod
    def is_authenticated(request: Request) -> bool:
        return request.session.get(SESSION_KEY, False)

    @staticmethod
    def deauthenticate(request: Request) -> None:
        request.session.pop(SESSION_KEY)
