from fastapi import Request

from market.database import Session
from market.database.models import ProductModel


SESSION_KEY = "clicked_products_list"
CLICKED: bool = True


class Clicks:
    @staticmethod
    def _is_already_counted(request: Request, product_id: int) -> bool:
        clicked_products: list | None = request.session.get(SESSION_KEY)

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

        with Session() as db:
            product: ProductModel = db.query(ProductModel).get(product_id)
            product.clicks += 1
            db.commit()

    @staticmethod
    def try_to_count(request: Request, product_id: int) -> None:
        if Clicks._is_already_counted(request, product_id):
            return

        Clicks._count(request, product_id)
