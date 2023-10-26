from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from market.database import Session
from market.database.models import (
    ProductModel,
    CategoryModel,
    ReviewModel,
    ReplyModel,
    BrandLinkModel,
    BrandModel
)
from settings import settings


class BrandView(ModelView):
    column_display_pk = True
    column_list = ("id", "name", "access_code")
    form_columns = ("name", "access_code")

    def __init__(self, session, **kwargs):
        super(BrandView, self).__init__(BrandModel, session, "Бренды", **kwargs)


class BrandLinkView(ModelView):
    column_display_pk = True
    form_columns = ("brand_id", "caption", "link")

    def __init__(self, session, **kwargs):
        super(BrandLinkView, self).__init__(BrandLinkModel, session, "Ссылки бренда", **kwargs)


class CategoryView(ModelView):
    column_display_pk = True
    column_list = ("id", "name")
    form_columns = ("name",)

    def __init__(self, session, **kwargs):
        super(CategoryView, self).__init__(CategoryModel, session, "Категории", **kwargs)


class ProductView(ModelView):
    column_display_pk = True
    column_list = ("id", "name", "clicks", "category_id", "brand_id")
    form_columns = ("category_id", "brand_id", "name", "description", "image_path", "clicks")

    def __init__(self, session, **kwargs):
        super(ProductView, self).__init__(ProductModel, session, "Товары", **kwargs)


class ReplyView(ModelView):
    column_display_pk = True
    column_list = ("id", "review_id", "reply", "posted_on")
    form_columns = ("review_id", "reply", "posted_on")

    def __init__(self, session, **kwargs):
        super(ReplyView, self).__init__(ReplyModel, session, "Ответы", **kwargs)


class ReviewView(ModelView):
    column_display_pk = True
    column_list = ("id", "product_id", "review", "rating", "posted_on")
    form_columns = ("product_id", "review", "rating", "posted_on")

    def __init__(self, session, **kwargs):
        super(ReviewView, self).__init__(ReviewModel, session, "Отзывы", **kwargs)


admin_app = Flask(__name__)
admin_app.secret_key = settings.secret_key

admin = Admin(admin_app, template_mode="bootstrap4", url="/")

flask_db = Session()

admin.add_view(BrandView(flask_db))
admin.add_view(BrandLinkView(flask_db))
admin.add_view(CategoryView(flask_db))
admin.add_view(ProductView(flask_db))
admin.add_view(ReplyView(flask_db))
admin.add_view(ReviewView(flask_db))
