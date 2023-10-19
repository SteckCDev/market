from random import randint, choice
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from settings import settings
from market.schemas.category import CategoryUI
from market.schemas.product import Product
from market.schemas.dummy import Dummy


app: FastAPI = FastAPI(
    title="Market Application",
    description="On-line catalog"
)

templates: Jinja2Templates = Jinja2Templates(directory=settings.template_folder)

app.mount("/static", StaticFiles(directory="market/static"), name="static")

# To be changed by actual database
# To be changed by actual database
# To be changed by actual database
categories: list[CategoryUI] = [
    CategoryUI(id=uuid4(), name=f"Category #{i}") for i in range(10)
]
products: list[Product] = [
    Product(
        id=uuid4(),
        category_id=choice(categories).id,
        brand_id=uuid4(),
        name=f"Product #{i}",
        description=f"some product by number {i}",
        clicks=randint(100, 999)
    ) for i in range(50)
]


def add_products_count():
    global categories
    global products

    for product in products:
        for category in categories:
            if product.category_id == category.id:
                category.products_count += 1


add_products_count()

# To be changed by actual database
# To be changed by actual database
# To be changed by actual database


@app.get("/auth")
def index(request: Request):
    context = {
        "request": request
    }

    return templates.TemplateResponse("base.html", context=context)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    context = {
        "request": request,
        "title": "Категории",
        "categories": categories
    }

    return templates.TemplateResponse("categories.html", context=context)


@app.get("/category/{category_id}")
def index(request: Request, category_id: UUID):
    context = {
        "request": request,
        "title": "Категории",
        "products": [product if product.category_id == category_id else None for product in products]
    }

    return templates.TemplateResponse("products.html", context=context)


@app.get("/product/{product_id}")
def index(product_id: UUID):
    return Dummy(page_name="card", data=[product_id])


@app.get("/feedback/{product_id}")
def index(product_id: UUID):
    return Dummy(page_name="feedback", data=[product_id])


@app.get("/feedback/service/{review_id}")
def index(review_id: UUID):
    return Dummy(page_name="feedback/service", data=[review_id])
