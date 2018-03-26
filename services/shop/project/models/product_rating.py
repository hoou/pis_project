from sqlalchemy import CheckConstraint, and_

from project import db


class ProductRating(db.Model):
    __tablename__ = 'product_ratings'
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    __table_args__ = (CheckConstraint(and_(rating >= 1, rating <= 5), name='check_rating_between_1_and_5'),)

    def __init__(self, rating: int):
        self.rating = rating
