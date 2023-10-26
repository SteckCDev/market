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
    form_columns = ("id", "name", "access_code")

    def __init__(self, session, **kwargs):
        super(BrandView, self).__init__(BrandModel, session, **kwargs)


class BrandLinkView(ModelView):
    form_columns = ("id", "brand_id", "caption", "link")

    def __init__(self, session, **kwargs):
        super(BrandLinkView, self).__init__(BrandLinkModel, session, **kwargs)


class CategoryView(ModelView):
    form_columns = ("id", "name")

    def __init__(self, session, **kwargs):
        super(CategoryView, self).__init__(CategoryModel, session, **kwargs)


class ProductView(ModelView):
    form_columns = ("id", "category_id", "brand_id", "name", "description", "image_path", "clicks")

    def __init__(self, session, **kwargs):
        super(ProductView, self).__init__(ProductModel, session, **kwargs)


class ReplyView(ModelView):
    form_columns = ("id", "review_id", "reply", "posted_on")

    def __init__(self, session, **kwargs):
        super(ReplyView, self).__init__(ReplyModel, session, **kwargs)


class ReviewView(ModelView):
    form_columns = ("id", "product_id", "review", "rating", "posted_on")

    def __init__(self, session, **kwargs):
        super(ReviewView, self).__init__(ReviewModel, session, **kwargs)


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
