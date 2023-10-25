from fastapi import Request

from common.database import DatabaseSQLite
from settings import settings


database = DatabaseSQLite(settings.database_path)

SESSION_KEY = "clicked_products_list"
CLICKED: bool = True


class Clicks:
    @staticmethod
    def _is_already_counted(request: Request, product_id: int) -> bool:
        clicked_products: list | None = request.session.get(SESSION_KEY)

        print(clicked_products)

        if clicked_products is None:
            return False

        return product_id in clicked_products

    @staticmethod
    def _count(request: Request, product_id: int):
        clicked_products: list | None = request.session.get(SESSION_KEY)

        if clicked_products is None:
            request.session[SESSION_KEY] = [product_id]
        else:
            request.session[SESSION_KEY].append(product_id)

        database.query("UPDATE products SET clicks = clicks + 1 WHERE id = ?", (product_id,))

    @staticmethod
    def try_to_count(request: Request, product_id: int) -> None:
        if Clicks._is_already_counted(request, product_id):
            return

        Clicks._count(request, product_id)
