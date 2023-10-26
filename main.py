from uuid import UUID

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette import status
from starlette.middleware.sessions import SessionMiddleware

from market.admin import admin_app
from market.contexts import (
    main_context_processor,
    get_reauth_context,
    get_index_context,
    get_category_context,
    get_product_context,
    get_feedback_context,
    get_service_feedback_context,
    get_admin_context,
)
from market.hooks.on_exception import (
    on_not_found_error,
    on_validation_error,
    on_internal_error
)
from market.middleware import RedirectToReauthMiddleware
from market.services import (
    Ads,
    Reauth,
    Reply,
    Review,
    Clicks,
    RecaptchaV2
)
from settings import settings


app: FastAPI = FastAPI(
    title="Market Application",
    description="On-line catalog",
    exception_handlers={
        status.HTTP_404_NOT_FOUND: on_not_found_error,
        RequestValidationError: on_validation_error,
        status.HTTP_500_INTERNAL_SERVER_ERROR: on_internal_error
    },
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)

app.add_middleware(
    RedirectToReauthMiddleware,
    reauth_path="/reauth",
    static_folder="/static",
    admin_path="/rulehere"
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    max_age=1800
)

app.mount("/admin", WSGIMiddleware(admin_app), name="admin")
app.mount("/static", StaticFiles(directory=settings.static_folder), name="static")
app.mount("/media", StaticFiles(directory=settings.media_folder), name="media")

templates: Jinja2Templates = Jinja2Templates(
    directory=settings.template_folder, context_processors=[main_context_processor]
)


@app.get("/reauth")
async def reauth(request: Request, redirect_to: str | None = None):
    return templates.TemplateResponse("reauth.html", context=get_reauth_context(request, redirect_to))


@app.post("/reauth")
async def reauth(
        request: Request,
        redirect_to: str = Form("/"),
        recaptcha_response: str = Form(..., alias="g-recaptcha-response")
):
    if not RecaptchaV2.verify_recaptcha(recaptcha_response, settings.recaptcha_secret_key):
        errors = ["Проверка на робота не пройдена, пожалуйста, попробуйте снова"]

        return templates.TemplateResponse(
            "reauth.html", context=get_reauth_context(request, redirect_to, errors=errors)
        )

    Reauth.authenticate(request)

    return RedirectResponse(redirect_to, status_code=status.HTTP_302_FOUND)


@app.get("/")
async def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", context=get_index_context(request))


@app.get("/category/{category_id}")
async def category(request: Request, category_id: int):
    return templates.TemplateResponse("category.html", context=get_category_context(request, category_id))


@app.get("/product/{product_id}")
async def products(request: Request, product_id: int):
    Clicks.try_to_count(request, product_id)

    return templates.TemplateResponse("product.html", context=get_product_context(request, product_id))


@app.get("/product/{product_id}/feedback")
async def feedback(request: Request, product_id: int):
    return templates.TemplateResponse("feedback.html", context=get_feedback_context(request, product_id))


@app.post("/product/{product_id}/feedback")
async def feedback(
        request: Request,
        product_id: int,
        review_body: str | None = Form(..., min_length=4, max_length=1024),
        review_rating: int | None = Form(..., ge=1, le=5),
        recaptcha_response: str = Form(..., alias="g-recaptcha-response")
):
    if not RecaptchaV2.verify_recaptcha(recaptcha_response, settings.recaptcha_secret_key):
        errors = ["Проверка на робота не пройдена, пожалуйста, попробуйте снова"]

        return templates.TemplateResponse(
            "feedback.html", context=get_feedback_context(request, product_id, errors=errors)
        )

    Review.create(product_id, review_body, review_rating)

    return RedirectResponse(f"/product/{product_id}", status_code=status.HTTP_302_FOUND)


@app.get("/product/{product_id}/feedback/{review_id}/reply/")
async def feedback_reply(request: Request, review_id: int):
    return templates.TemplateResponse("service_feedback.html", context=get_service_feedback_context(request, review_id))


@app.post("/product/{product_id}/feedback/{review_id}/reply/")
async def feedback_reply(
        request: Request,
        product_id: int,
        review_id: int,
        reply_body: str = Form(..., min_length=4, max_length=1024),
        reply_service_code: UUID = Form(...),
        recaptcha_response: str = Form(..., alias="g-recaptcha-response")
):
    if not RecaptchaV2.verify_recaptcha(recaptcha_response, settings.recaptcha_secret_key):
        errors = ["Проверка на робота не пройдена, пожалуйста, попробуйте снова"]

        return templates.TemplateResponse(
            "service_feedback.html", context=get_service_feedback_context(request, review_id, errors=errors)
        )

    if not Reply.compare_service_codes(product_id, reply_service_code):
        errors = ["Вы указали некорректный код сервиса"]

        return templates.TemplateResponse(
            "service_feedback.html", context=get_service_feedback_context(request, review_id, errors=errors)
        )

    Reply.create(review_id, reply_body)

    return RedirectResponse(f"/product/{product_id}", status_code=status.HTTP_302_FOUND)


@app.get("/rulehere")
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", context=get_admin_context(request))


@app.post("/rulehere")
async def admin(
        request: Request,
        ads_page_id: int = Form(...),
        ads_split: bool = Form(False),
        ads_link1: str | None = Form(None),
        ads_image1: UploadFile = File(...),
        ads_link2: str | None = Form(None),
        ads_image2: UploadFile = File(...),
        ads_enabled: bool = Form(False)
):
    await Ads.update(ads_page_id, ads_split, ads_link1, ads_image1, ads_link2, ads_image2, ads_enabled)

    return templates.TemplateResponse("admin.html", context=get_admin_context(request))
