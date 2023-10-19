from fastapi import Request

from common.database import DatabaseSQLite

from settings import settings
from .serializers import (
    serialize_index,
    serialize_category,
    serialize_product,
    serialize_reviews
)


database = DatabaseSQLite(settings.database_path)


def get_error_context(request: Request, error: str) -> dict:
    return {
        "request": request,
        "project_name": settings.project_name,
        "title": "Произошла ошибка",
        "error": error
    }


def get_reauth_context(request: Request, redirect_to: str) -> dict:
    return {
        "request": request,
        "project_name": settings.project_name,
        "title": "Проверка",
        "redirect_to": redirect_to
    }


def get_index_context(request: Request) -> dict:
    return {
        "request": request,
        "project_name": settings.project_name,
        "title": "Каталог",
        "categories": serialize_index()
    }


def get_category_context(request: Request, category_id: int) -> dict:
    raw_category_name = database.query("SELECT name FROM categories WHERE id = ?", (category_id,))

    category_name = None if len(raw_category_name) == 0 else raw_category_name[0][0]

    return {
        "request": request,
        "project_name": settings.project_name,
        "title": category_name,
        "products": serialize_category(category_id)
    }


def get_product_context(request: Request, product_id: int) -> dict:
    product = serialize_product(product_id)
    reviews = serialize_reviews(product_id)

    category_name = database.query("SELECT name FROM categories WHERE id = ?", (product.category_id,))[0][0]
    brand_links = database.query("SELECT links FROM brands WHERE id = ?", (str(product.brand_id),))[0][0]

    return {
        "request": request,
        "project_name": settings.project_name,
        "title": product.name,
        "product": product,
        "category_name": category_name,
        "brand_links": brand_links,
        "reviews": reviews
    }
