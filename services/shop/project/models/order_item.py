from project import db
from project.models.product import Product


class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product')

    def __init__(self, count: int, price: float, product_id: int):
        self.count = count
        self.price = price
        self.product_id = product_id
