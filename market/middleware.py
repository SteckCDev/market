from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .services.reauth import Reauth


class RedirectToReauthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, reauth_path: str, static_folder: str):
        super().__init__(app)
        self.reauth_path = reauth_path
        self.static_folder = static_folder

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith((self.reauth_path, self.static_folder)) or Reauth.is_authenticated(request):
            response = await call_next(request)
            return response

        return RedirectResponse(f"/reauth?redirect_to={request.url.path}")
