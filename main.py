from uuid import UUID

from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.middleware.sessions import SessionMiddleware

from market.contexts import (
    get_reauth_context,
    get_index_context,
    get_category_context,
    get_product_context,
    get_feedback_context,
    get_service_feedback_context
)
from market.hooks.on_exception import (
    on_not_found_error,
    on_validation_error,
    on_internal_error
)
from market.middleware import RedirectToReauthMiddleware
from market.services.review import Review
from market.services.reply import Reply
from settings import settings


app: FastAPI = FastAPI(
    title="Market Application",
    description="On-line catalog",
    exception_handlers={
        404: on_not_found_error,
        # TODO:
        422: on_validation_error,
        500: on_internal_error
    }
)

app.add_middleware(RedirectToReauthMiddleware, reauth_path=settings.reauth_path)
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, max_age=1800)

app.mount("/static", StaticFiles(directory=settings.static_folder), name="static")
app.mount("/media", StaticFiles(directory=settings.media_folder), name="media")

templates: Jinja2Templates = Jinja2Templates(directory=settings.template_folder)


@app.get("/reauth")
def auth(request: Request, redirect_to: str | None = None):
    return templates.TemplateResponse("reauth.html", context=get_reauth_context(request, redirect_to))


@app.post("/reauth")
def auth(request: Request, redirect_to: str | None = Form(...)):
    request.session["reauthenticated"] = 1

    return RedirectResponse("/" if redirect_to is None else redirect_to, status_code=status.HTTP_302_FOUND)


@app.get("/")
def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", context=get_index_context(request))


@app.get("/category/{category_id}")
def category(request: Request, category_id: int):
    return templates.TemplateResponse("category.html", context=get_category_context(request, category_id))


@app.get("/product/{product_id}")
def products(request: Request, product_id: int):
    return templates.TemplateResponse("product.html", context=get_product_context(request, product_id))


@app.get("/product/{product_id}/feedback")
def feedback(request: Request, product_id: int):
    return templates.TemplateResponse("feedback.html", context=get_feedback_context(request, product_id))


@app.post("/product/{product_id}/feedback")
def feedback(
        _request: Request,
        product_id: int,
        review_body: str | None = Form(..., min_length=4, max_length=1024),
        review_rating: int | None = Form(..., ge=1, le=5)
):
    Review.create(product_id, review_body, review_rating)

    return RedirectResponse(f"/product/{product_id}", status_code=status.HTTP_302_FOUND)


@app.get("/product/{product_id}/feedback/{review_id}/reply/")
def feedback_service(request: Request, review_id: int):
    return templates.TemplateResponse("service_feedback.html", context=get_service_feedback_context(request, review_id))


@app.post("/product/{product_id}/feedback/{review_id}/reply/")
def feedback_service(
        request: Request,
        product_id: int,
        review_id: int,
        reply_body: str = Form(..., min_length=4, max_length=1024),
        reply_service_code: UUID = Form(...)
):
    if Reply.compare_service_codes(product_id, reply_service_code):
        Reply.create(review_id, reply_body)

        return RedirectResponse(f"/product/{product_id}", status_code=status.HTTP_302_FOUND)
    else:
        errors = ["Вы указали некорректный код сервиса"]

        return templates.TemplateResponse(
            "service_feedback.html", context=get_service_feedback_context(request, review_id, errors=errors)
        )
