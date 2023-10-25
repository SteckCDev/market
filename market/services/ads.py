from os import path
from typing import Any
from uuid import uuid4

from fastapi import UploadFile

from market.database import Session
from market.database.models import AdModel
from settings import settings


class Ads:
    @staticmethod
    def _create_if_doesnt_exist(
            page_id: int,
            split: bool,
            link1: str | None,
            image1_path: str | None,
            link2: str | None,
            image2_path: str | None
    ) -> bool:
        with Session() as db:
            exists = db.query(AdModel).get(page_id) is not None

            if exists:
                return False

            _ad = AdModel(
                page_id=page_id, split=split, link1=link1, image1_path=image1_path, link2=link2, image2_path=image2_path
            )
            db.add(_ad)
            db.commit()

        return True

    @staticmethod
    async def _upload_image(image: UploadFile) -> str:
        image_bytes = await image.read()

        filename = str(uuid4())
        extension = image.filename.split(".")[-1]
        image_name = f"{filename}.{extension}"

        image_path = path.join(settings.media_folder, "commercials", image_name)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        image_url_path = f"media/commercials/{image_name}"

        return image_url_path

    @staticmethod
    async def update(
            page_id: int,
            split: bool,
            link1: str | None,
            image1: UploadFile,
            link2: str | None,
            image2: UploadFile,
            enabled: bool
    ) -> None:
        image1_path = await Ads._upload_image(image1) if image1.filename else None
        image2_path = await Ads._upload_image(image2) if image2.filename else None

        if Ads._create_if_doesnt_exist(page_id, split, link1, image1_path, link2, image2_path):
            return

        with Session() as db:
            _ad: AdModel = db.query(AdModel).get(page_id)

            _ad.split = split
            _ad.enabled = enabled

            if link1:
                _ad.link1 = link1

            if image1_path:
                _ad.image1_path = image1_path

            if link2:
                _ad.link2 = link2

            if image2_path:
                _ad.image2_path = image2_path

            db.commit()

    @staticmethod
    def get_for_page(page_id: int) -> dict[str, Any] | None:
        Ads._create_if_doesnt_exist(page_id, False, None, None, None, None)

        with Session() as db:
            return db.query(AdModel).get(page_id).__dict__
