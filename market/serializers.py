from typing import Optional

from fastapi.exceptions import HTTPException

from common.database import DatabaseSQLite

from settings import settings
from .schemas.category import CategoryUI
from .schemas.product import ProductUI
from .schemas.review import ReviewUI
from .schemas.reply import Reply


database = DatabaseSQLite(settings.database_path)


def _get_product_ui_additional(product_id: int, brand_id: int) -> tuple[str, float | None]:
    brand_name: str = database.query("SELECT name FROM brands WHERE id = ?", (brand_id,))[0][0]

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

    replies = []

    for reply_id, reply_body, reply_posted_on in raw_replies:
        replies.append(
            Reply(id=reply_id, review_id=review_id, reply=reply_body, posted_on=reply_posted_on)
        )

    return replies


def serialize_index() -> Optional[list[CategoryUI]]:
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


def serialize_category(category_id: int) -> Optional[list[ProductUI]]:
    raw_products = database.query(
        "SELECT id, brand_id, name, clicks FROM products WHERE category_id = ?", (category_id,)
    )

    if len(raw_products) == 0:
        return

    products = []

    for product_id, brand_id, product_name, product_clicks in raw_products:
        brand_name, rating = _get_product_ui_additional(product_id, brand_id)

        products.append(
            ProductUI(
                id=product_id, category_id=category_id, brand_id=brand_id, name=product_name, clicks=product_clicks,
                brand_name=brand_name, rating=rating
            )
        )

    return products


def serialize_product(product_id: int) -> ProductUI:
    raw_product = database.query(
        "SELECT id, category_id, brand_id, name, description, image_url, clicks FROM products WHERE id = ?",
        (product_id,)
    )

    if len(raw_product) == 0:
        raise HTTPException(status_code=404, detail=f"Requested product with id {product_id} that doesn't exist")

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

    reviews = []

    for review_id, review, rating, posted_on in raw_reviews:
        reviews.append(
            ReviewUI(
                id=review_id, product_id=product_id, review=review, rating=rating, posted_on=posted_on,
                replies=_get_replies_for_review(review_id)
            )
        )

    return reviews
