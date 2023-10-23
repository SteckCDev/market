from time import time
from uuid import UUID

from common.database import DatabaseSQLite
from settings import settings

database = DatabaseSQLite(settings.database_path)


class Reply:
    @staticmethod
    def create(review_id: int, reply: str) -> None:
        database.query(
            "INSERT INTO replies (review_id, reply, posted_on) VALUES (?, ?, ?)",
            (review_id, reply, int(time()))
        )

    @staticmethod
    def compare_service_codes(product_id: id, given_access_code: UUID) -> bool:
        access_code = database.query(
            "SELECT access_code FROM brands WHERE id = (SELECT brand_id FROM products WHERE id = ?)",
            (product_id,)
        )

        if len(access_code) == 0:
            return False

        print(given_access_code)
        print(access_code[0][0])

        return given_access_code == UUID(access_code[0][0])
