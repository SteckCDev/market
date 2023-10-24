from os import path
from uuid import uuid4

from fastapi import UploadFile

from common.database import DatabaseSQLite
from settings import settings

database = DatabaseSQLite(settings.database_path)


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
        exists = database.query("SELECT COUNT(*) FROM ads WHERE page_id = ?", (page_id,))[0][0] != 0

        if exists:
            return False

        database.query(
            "INSERT INTO ads (page_id, split, link1, image1_path, link2, image2_path) VALUES (?, ?, ?, ?, ?, ?)",
            (page_id, int(split), link1, image1_path, link2, image2_path)
        )

        return True

    @staticmethod
    async def update(
            page_id: int,
            split: bool,
            link1: str | None,
            image1: UploadFile,
            link2: str | None,
            image2: UploadFile
    ) -> None:
        image1_path = await Ads.upload_image(image1) if image1.filename else None
        image2_path = await Ads.upload_image(image2) if image2.filename else None

        if Ads._create_if_doesnt_exist(page_id, split, link1, image1_path, link2, image2_path):
            return

        data = [int(split),]
        query_data = ["split"]

        if link1:
            data.append(link1)
            query_data.append("link1")

        if image1_path:
            data.append(image1_path)
            query_data.append("image1_path")

        if link2:
            data.append(link2)
            query_data.append("link2")

        if image2_path:
            data.append(image2_path)
            query_data.append("image2_path")

        data.append(page_id)
        query = " = ?, ".join(query_data) + " = ?"

        database.query(
            f"UPDATE ads SET {query} WHERE page_id = ?", parameters=data
        )

    @staticmethod
    async def upload_image(image: UploadFile) -> str:
        image_bytes = await image.read()

        filename = str(uuid4())
        extension = image.filename.split(".")[-1]
        image_name = f"{filename}.{extension}"

        image_path = path.join(settings.media_folder, "ads", image_name)

        with open(image_path, "wb") as f:
            f.write(image_bytes)

        return image_path
