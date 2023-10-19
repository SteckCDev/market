import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from settings import settings
from market.on_exception import on_not_found_error, on_internal_error
from market.schemas.dummy import Dummy
from market.contexts import (
    get_reauth_context,
    get_index_context,
    get_category_context,
    get_product_context
)


app: FastAPI = FastAPI(
    title="Market Application",
    description="On-line catalog",
    exception_handlers={
        404: on_not_found_error,
        500: on_internal_error
    }
)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key, max_age=1800)

app.mount("/static", StaticFiles(directory=settings.static_folder), name="static")

templates: Jinja2Templates = Jinja2Templates(directory=settings.template_folder)


def reauth(request: Request) -> None:
    request.session["reauthenticated"] = 1


def redirect_to_reauth(request: Request) -> RedirectResponse | None:
    if request.session.get("reauthenticated") != 1:
        return RedirectResponse(f"/reauth?redirect_to={request.url.path}")


@app.get("/session")
def session(request: Request):
    return {"session": request.session}


@app.get("/reauth")
def auth(request: Request, redirect_to: str | None = None):
    return templates.TemplateResponse("reauth.html", context=get_reauth_context(request, redirect_to))


@app.post("/reauth")
def auth(request: Request, redirect_to: str | None = Form(...)):
    reauth(request)

    return RedirectResponse(redirect_to, status_code=302)


@app.get("/")
def index(request: Request) -> Response:
    to_redirect = redirect_to_reauth(request)

    if to_redirect:
        return to_redirect

    return templates.TemplateResponse("index.html", context=get_index_context(request))


@app.get("/category/{category_id}")
def category(request: Request, category_id: int):
    to_redirect = redirect_to_reauth(request)

    if to_redirect:
        return to_redirect

    return templates.TemplateResponse("category.html", context=get_category_context(request, category_id))


@app.get("/product/{product_id}")
def products(request: Request, product_id: int):
    to_redirect = redirect_to_reauth(request)

    if to_redirect:
        return to_redirect

    return templates.TemplateResponse("product.html", context=get_product_context(request, product_id))


@app.get("/feedback/{product_id}")
def feedback(request: Request, product_id: int):
    to_redirect = redirect_to_reauth(request)

    if to_redirect:
        return to_redirect

    return Dummy(page_name="feedback", data=[product_id])


@app.get("/feedback/service/{review_id}")
def feedback_service(request: Request, review_id: int):
    to_redirect = redirect_to_reauth(request)

    if to_redirect:
        return to_redirect

    return Dummy(page_name="feedback/service", data=[review_id])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
