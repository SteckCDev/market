from fastapi import Request
from fastapi.exceptions import HTTPException
from starlette import status

from common.database import DatabaseSQLite
from settings import settings
from .serializers import (
    serialize_index,
    serialize_category,
    serialize_product,
    serialize_reviews,
    serialize_review
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
        "main_caption": "Категории",
        "title": "Каталог",
        "categories": serialize_index()
    }


def get_category_context(request: Request, category_id: int) -> dict:
    raw_category_name = database.query("SELECT name FROM categories WHERE id = ?", (category_id,))

    category_name = None if len(raw_category_name) == 0 else raw_category_name[0][0]

    products = serialize_category(category_id)

    return {
        "request": request,
        "project_name": settings.project_name,
        "main_caption": f"{category_name} -> Все товары ({len(products)})" if products is not None else "",
        "title": category_name,
        "products": products
    }


def get_product_context(request: Request, product_id: int) -> dict:
    product = serialize_product(product_id)
    reviews = serialize_reviews(product_id)

    category_name = database.query("SELECT name FROM categories WHERE id = ?", (product.category_id,))[0][0]
    raw_brand_links = database.query("SELECT links FROM brands WHERE id = ?", (str(product.brand_id),))[0][0]

    if raw_brand_links is None:
        brand_links = None
    else:
        brand_links = [link_with_caption.split(">;<") for link_with_caption in raw_brand_links.split("<;>")]

    return {
        "request": request,
        "project_name": settings.project_name,
        "main_caption": f"{category_name} -> {product.id:06}",
        "title": product.name,
        "product": product,
        "category_name": category_name,
        "brand_links": brand_links,
        "reviews": reviews,
        "reviews_count": len(reviews) if reviews is not None else 0
    }


def get_feedback_context(request: Request, product_id: int) -> dict:
    product = serialize_product(product_id)

    category_name = database.query("SELECT name FROM categories WHERE id = ?", (product.category_id,))[0][0]

    return {
        "request": request,
        "project_name": settings.project_name,
        "main_caption": f"{category_name} -> {product.id:06} -> Оставить отзыв"
    }


def get_service_feedback_context(request: Request, review_id: int, errors: list[str] | None = None) -> dict:
    review = serialize_review(review_id)

    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    category_name = database.query(
        "SELECT name FROM categories WHERE id = (SELECT category_id FROM products WHERE id = ?)", (review.product_id,)
    )[0][0]

    return {
        "request": request,
        "project_name": settings.project_name,
        "main_caption": f"{category_name} -> {review.product_id:06} -> Ответить на отзыв #{review_id}",
        "review": review,
        "errors": errors
    }
