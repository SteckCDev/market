from uuid import UUID
from typing import Optional

from fastapi.exceptions import HTTPException
from starlette import status

from common.database import DatabaseSQLite
from settings import settings
from .services.ads import Ads
from .schemas.category import Category, CategoryUI
from .schemas.product import ProductUI
from .schemas.reply import Reply
from .schemas.review import ReviewUI
from .schemas.ad import Ad, AdUI
from .schemas.brand_link import BrandLink


database = DatabaseSQLite(settings.database_path)


def _get_product_ui_additional(product_id: int, brand_id: int) -> tuple[str, float | None]:
    brand_name = database.query("SELECT name FROM brands WHERE id = ?", (brand_id,))[0][0]

    raw_reviews = database.query("SELECT rating FROM reviews WHERE product_id = ?", (product_id,))

    if len(raw_reviews) != 0:
        total_rating = 0

        for review in raw_reviews:
            total_rating += review[0]

        rating = round(total_rating / len(raw_reviews), 1)
    else:
        rating = None

    return brand_name, rating


def _get_replies_for_review(review_id: int) -> Optional[list[Reply]]:
    raw_replies = database.query("SELECT id, reply, posted_on FROM replies WHERE review_id = ?", (review_id,))

    if len(raw_replies) == 0:
        return

    return [
        Reply(
            id=_id, review_id=review_id, reply=reply_body, posted_on=reply_posted_on
        ) for _id, reply_body, reply_posted_on in raw_replies
    ]


def serialize_categories() -> Optional[list[CategoryUI]]:
    raw_categories = database.query("SELECT id, name FROM categories")

    if len(raw_categories) == 0:
        return

    categories = []

    for category_id, category_name in raw_categories:
        products_count = database.query(
            "SELECT COUNT(*) FROM products WHERE category_id = ?", (category_id,)
        )[0][0]

        if products_count == 0:
            continue

        categories.append(
            CategoryUI(
                id=category_id, name=category_name, products_count=products_count
            )
        )

    return categories


def serialize_products(category_id: int) -> Optional[list[ProductUI]]:
    raw_products = database.query(
        "SELECT id, brand_id, name, image_url, clicks FROM products WHERE category_id = ?", (category_id,)
    )

    if len(raw_products) == 0:
        return

    products = []

    for product_id, brand_id, product_name, image_url, product_clicks in raw_products:
        brand_name, rating = _get_product_ui_additional(product_id, brand_id)

        products.append(
            ProductUI(
                id=product_id, category_id=category_id, brand_id=brand_id, name=product_name, image_url=image_url,
                clicks=product_clicks, brand_name=brand_name, rating=rating
            )
        )

    return products


def serialize_single_product(product_id: int) -> ProductUI:
    raw_product = database.query(
        "SELECT id, category_id, brand_id, name, description, image_url, clicks FROM products WHERE id = ?",
        (product_id,)
    )

    if len(raw_product) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested product with id {product_id} that doesn't exist"
        )

    product_id, category_id, brand_id, name, description, image_url, clicks = raw_product[0]
    brand_name, rating = _get_product_ui_additional(product_id, brand_id)

    return ProductUI(
        id=product_id, category_id=category_id, brand_id=brand_id, name=name, clicks=clicks,
        brand_name=brand_name, rating=rating, description=description, image_url=image_url
    )


def serialize_reviews(product_id: int) -> Optional[list[ReviewUI]]:
    raw_reviews = database.query(
        "SELECT id, review, rating, posted_on FROM reviews WHERE product_id = ?", (product_id,)
    )

    if len(raw_reviews) == 0:
        return

    return [
        ReviewUI(
            id=_id, product_id=product_id, review=review, rating=rating, posted_on=posted_on,
            replies=_get_replies_for_review(_id)
        ) for _id, review, rating, posted_on in raw_reviews
    ]


def serialize_single_review(review_id: int) -> ReviewUI:
    raw_review = database.query(
        "SELECT product_id, review, rating, posted_on FROM reviews WHERE id = ?", (review_id,)
    )

    if len(raw_review) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested review with id {review_id} that doesn't exist"
        )

    product_id, review, rating, posted_on = raw_review[0]

    return ReviewUI(id=review_id, product_id=product_id, review=review, rating=rating, posted_on=posted_on)


def serialize_brand_links(brand_id: UUID) -> Optional[list[BrandLink]]:
    raw_brand_links = database.query(
        "SELECT id, brand_id, caption, link FROM brand_links WHERE brand_id = ?", (str(brand_id),)
    )

    if len(raw_brand_links) == 0:
        return

    return [
        BrandLink(
            id=_id, brand_id=brand_id, caption=caption, link=link
        ) for _id, brand_id, caption, link in raw_brand_links
    ]


def serialize_ads_for_page(page_id: int) -> Ad:
    return Ad(**Ads.get_for_page(page_id))


def serialize_ads_for_admin(pages_ids: dict[int, str]) -> list[AdUI]:
    return [AdUI(**Ads.get_for_page(page_id), name=page_name) for page_id, page_name in pages_ids.items()]


def serialize_categories_for_admin() -> Optional[list[Category]]:
    raw_categories = database.query("SELECT id, name FROM categories")

    if len(raw_categories) == 0:
        return

    return [Category(id=_id, name=name) for _id, name in raw_categories]
