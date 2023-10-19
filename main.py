from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from settings import settings
from market.on_exception import on_not_found_error, on_internal_error
from market.schemas.dummy import Dummy
from market.contexts import (
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

app.mount("/static", StaticFiles(directory=settings.static_folder), name="static")

templates: Jinja2Templates = Jinja2Templates(directory=settings.template_folder)


@app.get("/auth")
def auth(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("base.html", context=context)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", context=get_index_context(request))


@app.get("/category/{category_id}")
def category(request: Request, category_id: int):
    return templates.TemplateResponse("category.html", context=get_category_context(request, category_id))


@app.get("/product/{product_id}")
def products(request: Request, product_id: int):
    return templates.TemplateResponse("product.html", context=get_product_context(request, product_id))


@app.get("/feedback/{product_id}")
def feedback(product_id: int):
    return Dummy(page_name="feedback", data=[product_id])


@app.get("/feedback/service/{review_id}")
def feedback_service(review_id: int):
    return Dummy(page_name="feedback/service", data=[review_id])
