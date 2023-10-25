from market.database import Session
from market.database.models import ReviewModel


class Review:
    @staticmethod
    def create(product_id: int, review: str, rating: int) -> None:
        with Session() as db:
            _review = ReviewModel(product_id=product_id, review=review, rating=rating)
            db.add(_review)
            db.commit()
