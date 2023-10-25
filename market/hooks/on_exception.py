from contextlib import suppress

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from starlette import status

from market.contexts import (
    get_error_context,
    get_feedback_context,
    get_service_feedback_context
)
from settings import settings


templates: Jinja2Templates = Jinja2Templates(directory=settings.template_folder)


def _parse_feedback_errors(exc: HTTPException) -> list[str]:
    errors = []

    with suppress(KeyError, TypeError, ValueError):
        for error in exc.__dict__.get("_errors"):
            match error.get("loc")[1], error.get("type"):
                case "review_body", "string_too_short":
                    errors.append("Текст отзыва слишком короткий")
                case "review_body", "string_too_long":
                    errors.append("Текст отзыва слишком длинный")
                case "review_rating", "missing":
                    errors.append("Пожалуйста, дайте оценку товару")
                case "g-recaptcha-response", "missing":
                    errors.append("Пожалуйста, пройдите проверку на робота")

    return errors if len(errors) != 0 else ["Пожалуйста, проверьте введённую информацию"]


def _parse_service_feedback_errors(exc: HTTPException) -> list[str]:
    errors = []

    with suppress(KeyError, TypeError, ValueError):
        for error in exc.__dict__.get("_errors"):
            match error.get("loc")[1], error.get("type"):
                case "reply_body", "string_too_short":
                    errors.append("Текст ответа слишком короткий")
                case "reply_body", "string_too_long":
                    errors.append("Текст ответа слишком длинный")
                case "reply_service_code", "uuid_parsing":
                    errors.append("Пожалуйста, укажите корректный код сервиса")
                case "g-recaptcha-response", "missing":
                    errors.append("Пожалуйста, пройдите проверку на робота")

    return errors if len(errors) != 0 else ["Пожалуйста, проверьте введённую информацию"]


def on_not_found_error(request: Request, _exc: HTTPException):
    errors = ["Страница не найдена"]

    return templates.TemplateResponse(
        "error.html", context=get_error_context(request, errors=errors),
        status_code=status.HTTP_404_NOT_FOUND
    )


def on_validation_error(request: Request, exc: HTTPException):
    """ Bad code below :) """

    if "/product" in request.url.path and "/feedback" in request.url.path and "/reply" in request.url.path:
        try:
            review_id = int("".join(filter(str.isdigit, request.url.path.split("feedback")[1])))
        except (ValueError, KeyError):
            return RedirectResponse(request.url.path)

        errors = _parse_service_feedback_errors(exc)

        return templates.TemplateResponse(
            "service_feedback.html", context=get_service_feedback_context(request, review_id, errors=errors)
        )

    elif "/product" in request.url.path and "/feedback" in request.url.path:
        try:
            product_id = int("".join(filter(str.isdigit, request.url.path)))
        except ValueError:
            return RedirectResponse(request.url.path)

        errors = _parse_feedback_errors(exc)

        return templates.TemplateResponse(
            "feedback.html", context=get_feedback_context(request, product_id, errors=errors)
        )

    errors = ["Мы вас не поняли"]

    return templates.TemplateResponse(
        "error.html", context=get_error_context(request, errors=errors),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def on_internal_error(request: Request, _exc: HTTPException):
    errors = [
        "У нас неполадки, если эта ошибка мешает вам сделать что-то важное, обратитесь в техническую поддержку"
    ]

    return templates.TemplateResponse(
        "error.html", context=get_error_context(request, errors=errors),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
