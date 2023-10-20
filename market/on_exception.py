from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates

from settings import settings
from .contexts import get_error_context


templates: Jinja2Templates = Jinja2Templates(directory=settings.template_folder)


def on_not_found_error(request: Request, exc: HTTPException):
    error = "404: страница не найдена"

    return templates.TemplateResponse(
        "error.html", context=get_error_context(request, error), status_code=404
    )


def on_validation_error(request: Request, exc: HTTPException):
    error = "422: мы вас не поняли"

    return templates.TemplateResponse(
        "error.html", context=get_error_context(request, error), status_code=422
    )


def on_internal_error(request: Request, exc: HTTPException):
    error = "500: у нас неполадки, если эта ошибка мешает вам сделать что-то важное, обратитесь в техническую поддержку"

    return templates.TemplateResponse(
        "error.html", context=get_error_context(request, error), status_code=500
    )
