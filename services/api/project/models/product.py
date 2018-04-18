from sqlalchemy import CheckConstraint

from project import db
from project.models.product_image import ProductImage


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean(), default=False)
    images = db.relationship('ProductImage', backref='product', lazy=True)
    ratings = db.relationship('ProductRating', backref='product', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship("Category")
    __table_args__ = (CheckConstraint(count >= 0, name='check_count_geq_zero'),)

    def __init__(self, name, price, count=0, description=None):
        self.name = name
        self.price = price
        self.count = count
        self.description = description
