from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RedirectToReauth(BaseHTTPMiddleware):
    def __init__(self, app, reauth_path: str):
        super().__init__(app)
        self.reauth_path = reauth_path

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(self.reauth_path) or request.session.get("reauthenticated") == 1:
            response = await call_next(request)
            return response

        return RedirectResponse(f"/reauth?redirect_to={request.url.path}")
