from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from .services.admin import Admin
from .services.reauth import Reauth
from .hooks.on_exception import on_not_found_error


class RedirectToReauthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, reauth_path: str, static_folder: str, admin_path: str):
        super().__init__(app)
        self.reauth_path = reauth_path
        self.static_folder = static_folder
        self.admin_path = admin_path

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if request.url.path.startswith(self.admin_path) and not Admin.is_authenticated(request):
            if Reauth.is_authenticated(request):
                return on_not_found_error(request, HTTPException(status_code=404))
            else:
                return RedirectResponse(f"/reauth?redirect_to={request.url.path}")

        allowed_anyway = request.url.path.startswith((self.reauth_path, self.static_folder))

        if not allowed_anyway and not Reauth.is_authenticated(request):
            return RedirectResponse(f"/reauth?redirect_to={request.url.path}")

        return response
