from fastapi import Request, HTTPException
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette import status

from .services import (
    AdminAuth,
    Reauth
)
from market.hooks.on_exception import on_not_found_error


class RedirectToReauthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, reauth_path: str, static_folder: str, admin_path: str, rulehere_path: str):
        super().__init__(app)
        self.reauth_path = reauth_path
        self.static_folder = static_folder
        self.admin_path = admin_path
        self.rulehere_path = rulehere_path

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        is_admin_path = request.url.path.startswith((self.admin_path, self.rulehere_path))
        is_auth_page = request.url.path == f"{self.rulehere_path}/auth"

        if is_admin_path and not AdminAuth.is_authenticated(request) and not is_auth_page:
            if Reauth.is_authenticated(request):
                return on_not_found_error(request, HTTPException(status_code=status.HTTP_404_NOT_FOUND))
            else:
                return RedirectResponse(f"/reauth?redirect_to={request.url.path}")

        allowed_anyway = request.url.path.startswith((self.reauth_path, self.static_folder))

        if not allowed_anyway and not Reauth.is_authenticated(request):
            return RedirectResponse(f"/reauth?redirect_to={request.url.path}")

        return response
