from project import db


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    images = db.relationship('ProductImage', backref='product', lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, name, price, description=None):
        self.name = name
        self.price = price
        self.description = description
