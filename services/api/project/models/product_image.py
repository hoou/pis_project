from project import db


class ProductImage(db.Model):
    __tablename__ = "product_images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __init__(self, url):
        self.url = url
