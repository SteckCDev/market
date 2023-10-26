from fastapi import Request

from os import path
from typing import Any
from uuid import uuid4

from fastapi import UploadFile

from market.database import Session
from market.database.models import ProductModel

from settings import settings


SESSION_KEY: str = "superuser"
AUTHENTICATED: bool = True


class AdminAuth:
    @staticmethod
    def check_credentials(login: str, password: str) -> bool:
        return login == settings.admin_login and password == settings.admin_password

    @staticmethod
    def authenticate(request: Request) -> None:
        request.session[SESSION_KEY] = AUTHENTICATED

    @staticmethod
    def is_authenticated(request: Request) -> bool:
        return request.session.get(SESSION_KEY, False)

    @staticmethod
    def deauthenticate(request: Request) -> None:
        request.session.pop(SESSION_KEY)


class AdminProducts:
    @staticmethod
    async def _upload_image(product_id: int, image: UploadFile) -> str:
        image_bytes = await image.read()

        extension = image.filename.split(".")[-1]
        image_name = f"{product_id}.{extension}"

        image_path = path.join(settings.media_folder, "products", image_name)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_url_path = f"/media/products/{image_name}"

        return image_url_path

    @staticmethod
    async def set_image(product_id: int, image: UploadFile) -> None:
        image_path = await AdminProducts._upload_image(product_id, image) if image.filename else None

        with Session() as db:
            product: ProductModel | None = db.get(ProductModel, product_id)

            if product is None:
                return

            product.image_path = image_path

            db.commit()
