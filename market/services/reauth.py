from fastapi import Request


class Reauth:
    SESSION_KEY: str = "reauthenticated"
    AUTHENTICATED: bool = True

    @staticmethod
    def authenticate(request: Request) -> None:
        request.session[Reauth.SESSION_KEY] = Reauth.AUTHENTICATED

    @staticmethod
    def is_authenticated(request: Request) -> bool:
        return request.session.get(Reauth.SESSION_KEY, False)

    @staticmethod
    def deauthenticate(request: Request) -> None:
        request.session.pop(Reauth.SESSION_KEY)
