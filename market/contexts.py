from typing import Any

from fastapi import Request

from common.database import DatabaseSQLite
from settings import settings
from .serializers import (
    serialize_categories,
    serialize_products,
    serialize_single_product,
    serialize_reviews,
    serialize_single_review
)


database = DatabaseSQLite(settings.database_path)


def get_error_context(request: Request, error: str) -> dict[str, Any]:
    return {
        "request": request,
        "title": "Произошла ошибка",
        "error": error
    }


def get_reauth_context(request: Request, redirect_to: str | None, errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "request": request,
        "title": "Продолжить в каталог",
        "redirect_to": "" if redirect_to is None else redirect_to,
        "recaptcha_site_key": settings.recaptcha_site_key,
        "errors": errors
    }


def get_index_context(request: Request) -> dict[str, Any]:
    return {
        "request": request,
        "main_caption": "Категории товаров",
        "title": "Каталог",
        "categories": serialize_categories()
    }


def get_category_context(request: Request, category_id: int) -> dict[str, Any]:
    raw_category_name = database.query("SELECT name FROM categories WHERE id = ?", (category_id,))

    category_name = None if len(raw_category_name) == 0 else raw_category_name[0][0]

    products = serialize_products(category_id)

    return {
        "request": request,
        "main_caption": f"{category_name} -> Все товары ({len(products)})" if products is not None else "",
        "title": category_name,
        "products": products
    }


def get_product_context(request: Request, product_id: int) -> dict[str, Any]:
    product = serialize_single_product(product_id)
    reviews = serialize_reviews(product_id)

    category_name = database.query("SELECT name FROM categories WHERE id = ?", (product.category_id,))[0][0]
    raw_brand_links = database.query("SELECT links FROM brands WHERE id = ?", (str(product.brand_id),))[0][0]

    if raw_brand_links is None:
        brand_links = None
    else:
        brand_links = [link_with_caption.split(">;<") for link_with_caption in raw_brand_links.split("<;>")]

    return {
        "request": request,
        "main_caption": f"{category_name} -> {product.id:06}",
        "title": product.name,
        "product": product,
        "category_name": category_name,
        "brand_links": brand_links,
        "reviews": reviews,
        "reviews_count": len(reviews) if reviews is not None else 0
    }


def get_feedback_context(request: Request, product_id: int, errors: list[str] | None = None) -> dict[str, Any]:
    product = serialize_single_product(product_id)

    category_name = database.query("SELECT name FROM categories WHERE id = ?", (product.category_id,))[0][0]

    return {
        "request": request,
        "main_caption": f"{category_name} -> {product.id:06} -> Оставить отзыв",
        "title": f"Оставить отзыв о {product.name}",
        "recaptcha_site_key": settings.recaptcha_site_key,
        "errors": errors
    }


def get_service_feedback_context(request: Request, review_id: int, errors: list[str] | None = None) -> dict[str, Any]:
    review = serialize_single_review(review_id)

    category_name = database.query(
        "SELECT name FROM categories WHERE id = (SELECT category_id FROM products WHERE id = ?)", (review.product_id,)
    )[0][0]

    return {
        "request": request,
        "main_caption": f"{category_name} -> {review.product_id:06} -> Ответить на отзыв #{review_id}",
        "title": "Ответить на отзыв",
        "recaptcha_site_key": settings.recaptcha_site_key,
        "review": review,
        "errors": errors
    }


def get_admin_context(request: Request) -> dict[str, Any]:
    ads_pages = {
        1: "Страница входа",
        2: "Страница всех категорий",
        3: "Страница категории",
        4: "Страница товара",
        5: "Страница \"Оставить отзыв\"",
        6: "Страница \"Ответить на отзыв\""
    }

    return {
        "request": request,
        "ads_pages": ads_pages
    }
