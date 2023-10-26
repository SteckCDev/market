from typing import Optional
from uuid import UUID

from fastapi.exceptions import HTTPException
from sqlalchemy.orm.query import Query
from starlette import status

from market.database import Session
from .database.models import (
    BrandModel,
    ReplyModel,
    ReviewModel,
    CategoryModel,
    ProductModel,
    BrandLinkModel
)
from .schemas import (
    Ad,
    AdUI,
    BrandLink,
    Category,
    CategoryUI,
    ProductUI,
    Reply,
    ReviewUI
)
from .services.ads import Ads


def _get_product_ui_additional(product_id: int, brand_id: int) -> tuple[str, float | None]:
    with Session() as db:
        brand: BrandModel = db.query(BrandModel).get(brand_id)
        reviews: Query[ReviewModel] | None = db.query(ReviewModel).filter(ReviewModel.product_id == product_id)

    reviews_count = reviews.count()

    if reviews_count == 0:
        return brand.name, None

    total_rating = sum([review.rating for review in reviews])
    rating = round(total_rating / reviews_count, 1)

    return brand.name, rating


def _get_replies_for_review(review_id: int) -> Optional[list[Reply]]:
    with Session() as db:
        replies: Query[ReplyModel] = db.query(ReplyModel).filter(ReplyModel.review_id == review_id)

    if replies.count() == 0:
        return

    return [Reply(**reply.__dict__) for reply in replies]


def serialize_categories() -> Optional[list[CategoryUI]]:
    with Session() as db:
        categories: list[CategoryModel] = db.query(CategoryModel).all()

        if len(categories) == 0:
            return

        categories_ui = []

        for category in categories:
            products_count = db.query(ProductModel).filter(ProductModel.category_id == category.id).count()

            if products_count == 0:
                continue

            categories_ui.append(
                CategoryUI(id=category.id, name=category.name, products_count=products_count)
            )

    return categories_ui


def serialize_products(category_id: int) -> Optional[list[ProductUI]]:
    with Session() as db:
        products: Query[ProductModel] = db.query(ProductModel).filter(ProductModel.category_id == category_id)

    if products.count() == 0:
        return

    products_ui = []

    for product in products:
        brand_name, rating = _get_product_ui_additional(product.id, product.brand_id)

        products_ui.append(
            ProductUI(**product.__dict__, brand_name=brand_name, rating=rating)
        )

    return products_ui


def serialize_single_product(product_id: int) -> ProductUI:
    with Session() as db:
        product: ProductModel | None = db.get(ProductModel, product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested product with id {product_id} that doesn't exist"
        )

    brand_name, rating = _get_product_ui_additional(product.id, product.brand_id)

    return ProductUI(**product.__dict__, brand_name=brand_name, rating=rating)


def serialize_reviews(product_id: int) -> Optional[list[ReviewUI]]:
    with Session() as db:
        reviews: Query[ReviewModel] = db.query(ReviewModel).filter(ReviewModel.product_id == product_id)

    if reviews.count() == 0:
        return

    return [ReviewUI(**review.__dict__, replies=_get_replies_for_review(review.id)) for review in reviews]


def serialize_single_review(review_id: int) -> ReviewUI:
    with Session() as db:
        review: ReviewModel | None = db.get(ReviewModel, review_id)

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Requested review with id {review_id} that doesn't exist"
        )

    return ReviewUI(**review.__dict__)


def serialize_brand_links(brand_id: int) -> Optional[list[BrandLink]]:
    with Session() as db:
        brand_links: Query[BrandLinkModel] = db.query(BrandLinkModel).filter(BrandLinkModel.brand_id == brand_id)

    if brand_links.count() == 0:
        return

    return [BrandLink(**brand_link.__dict__) for brand_link in brand_links]


def serialize_ads_for_page(page_id: int) -> Ad:
    return Ad(**Ads.get_for_page(page_id))


def serialize_ads_for_admin(pages_ids: dict[int, str]) -> list[AdUI]:
    return [AdUI(**Ads.get_for_page(page_id), name=page_name) for page_id, page_name in pages_ids.items()]


def serialize_categories_for_admin() -> Optional[list[Category]]:
    with Session() as db:
        categories: list[CategoryModel] = db.query(CategoryModel).all()

    if len(categories) == 0:
        return

    return [Category(**category.__dict__) for category in categories]
