from time import time

from common.database import DatabaseSQLite
from settings import settings


database = DatabaseSQLite(settings.database_path)


class Review:
    @staticmethod
    def create(product_id: int, review: str, rating: int) -> None:
        database.query(
            "INSERT INTO reviews (product_id, review, rating, posted_on) VALUES (?, ?, ?, ?)",
            (product_id, review, rating, int(time()))
        )
