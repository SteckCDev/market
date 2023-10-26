from typing import Any

from fastapi import Request

from market.database import Session
from market.database.models import (
    CategoryModel,
    ProductModel
)
from settings import settings
from .serializers import (
    serialize_categories,
    serialize_products,
    serialize_single_product,
    serialize_reviews,
    serialize_single_review,
    serialize_brand_links,
    serialize_ads_for_page,
    serialize_ads_for_admin,
)
from market.services import AdminAuth


def main_context_processor(request: Request) -> dict[str, Any]:
    return {
        "project_name": settings.project_name,
        "rules_link": settings.rules_link,
        "news_link": settings.news_link,
        "offer_link": settings.offer_link,
        "stats_link": settings.stats_link,
        "chat_link": settings.chat_link,
        "about_link": settings.about_link,
        "admin_link": "/admin" if AdminAuth.is_authenticated(request) else None,
        "rulehere_link": "/rulehere" if AdminAuth.is_authenticated(request) else None
    }


def get_error_context(request: Request, errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "request": request,
        "title": "Произошла ошибка",
        "errors": errors
    }


def get_reauth_context(request: Request, redirect_to: str | None, errors: list[str] | None = None) -> dict[str, Any]:
    page_id = 1

    return {
        "request": request,
        "title": "Продолжить в каталог",
        "ads": serialize_ads_for_page(page_id),
        "redirect_to": "" if redirect_to is None else redirect_to,
        "recaptcha_site_key": settings.recaptcha_site_key,
        "errors": errors
    }


def get_index_context(request: Request) -> dict[str, Any]:
    page_id = 2

    return {
        "request": request,
        "main_caption": "Категории товаров",
        "title": "Каталог",
        "ads": serialize_ads_for_page(page_id),
        "categories": serialize_categories()
    }


def get_category_context(request: Request, category_id: int) -> dict[str, Any]:
    page_id = 3

    with Session() as db:
        category: CategoryModel | None = db.get(CategoryModel, category_id)

    category_name = None if category is None else category.name

    products = serialize_products(category_id)

    return {
        "request": request,
        "main_caption": f"{category_name} -> Все товары ({len(products)})" if products is not None else "",
        "title": category_name,
        "ads": serialize_ads_for_page(page_id),
        "products": products
    }


def get_product_context(request: Request, product_id: int) -> dict[str, Any]:
    page_id = 4

    product = serialize_single_product(product_id)
    reviews = serialize_reviews(product_id)

    with Session() as db:
        category: CategoryModel | None = db.get(CategoryModel, product.category_id)

    category_name = None if category is None else category.name

    return {
        "request": request,
        "main_caption": f"{category_name} -> {product.id:06}",
        "title": product.name,
        "ads": serialize_ads_for_page(page_id),
        "product": product,
        "category_name": category_name,
        "brand_links": serialize_brand_links(product.brand_id),
        "reviews": reviews,
        "reviews_count": len(reviews) if reviews is not None else 0
    }


def get_feedback_context(request: Request, product_id: int, errors: list[str] | None = None) -> dict[str, Any]:
    page_id = 5

    product = serialize_single_product(product_id)

    with Session() as db:
        category: CategoryModel | None = db.get(CategoryModel, product.category_id)

    category_name = None if category is None else category.name

    return {
        "request": request,
        "main_caption": f"{category_name} -> {product.id:06} -> Оставить отзыв",
        "title": f"Оставить отзыв о {product.name}",
        "ads": serialize_ads_for_page(page_id),
        "recaptcha_site_key": settings.recaptcha_site_key,
        "errors": errors
    }


def get_service_feedback_context(request: Request, review_id: int, errors: list[str] | None = None) -> dict[str, Any]:
    page_id = 6

    review = serialize_single_review(review_id)

    with Session() as db:
        product: ProductModel | None = db.get(ProductModel, review.product_id)

        if product is not None:
            category: CategoryModel | None = db.get(CategoryModel, product.category_id)
        else:
            category = None

    category_name = None if category is None else category.name

    return {
        "request": request,
        "main_caption": f"{category_name} -> {review.product_id:06} -> Ответить на отзыв #{review_id}",
        "title": "Ответить на отзыв",
        "ads": serialize_ads_for_page(page_id),
        "recaptcha_site_key": settings.recaptcha_site_key,
        "review": review,
        "errors": errors
    }


def get_admin_auth_context(request: Request, errors: list[str] | None = None) -> dict[str, Any]:
    return {
        "request": request,
        "recaptcha_site_key": settings.recaptcha_site_key,
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
        "ads_for_admin": serialize_ads_for_admin(ads_pages)
    }
