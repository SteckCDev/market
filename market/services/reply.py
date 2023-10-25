from uuid import UUID

from market.database import Session
from market.database.models import (
    ReplyModel,
    BrandModel,
    ProductModel
)


class Reply:
    @staticmethod
    def create(review_id: int, reply: str) -> None:
        with Session() as db:
            _reply = ReplyModel(review_id=review_id, reply=reply)
            db.add(_reply)
            db.commit()

    @staticmethod
    def compare_service_codes(product_id: id, given_access_code: UUID) -> bool:
        with Session() as db:
            product: ProductModel = db.query(ProductModel).get(product_id)
            brand: BrandModel = db.query(BrandModel).get(product.brand_id)

        if brand.access_code is None:
            return False

        return bool(given_access_code == brand.access_code)
