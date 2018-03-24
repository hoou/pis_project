from project import db


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    products = db.relationship('Product', backref='product', lazy=True)

    # parent_category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    # child_categories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy='joined')

    def __init__(self, name, parent_category_id=None):
        self.name = name
        # self.parent_category_id = parent_category_id
