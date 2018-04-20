from sqlalchemy.orm import Session

from project import db
from project.models.product import Product
from project.models.product_image import ProductImage
from project.models.product_rating import ProductRating
from project.models.user import User

session: Session = db.session


def get_all():
    return Product.query.filter_by(is_deleted=False).all()


def get_all_deleted():
    return Product.query.filter_by(is_deleted=True).all()


def get(product_id):
    return Product.query.filter_by(id=product_id, is_deleted=False).first()


def get_deleted(product_id):
    return Product.query.filter_by(id=product_id, is_deleted=True).first()


def delete(product: Product):
    product.is_deleted = True
    session.commit()


def restore(product: Product):
    product.is_deleted = False
    session.commit()


def add_image(product: Product, **kwargs):
    image = ProductImage(**kwargs)
    image.product_id = product.id
    product.images += [image]
    session.commit()
    return image


def get_images(product_id):
    return ProductImage.query.filter_by(product_id=product_id).all()


def delete_image(image_id):
    session.delete(ProductImage.query.filter_by(id=image_id).first())
    session.commit()


def has_image(product_id, image_id):
    product_images = get_images(product_id)
    image = ProductImage.query.filter_by(id=image_id).first()
    return image in product_images


def add_rating(product: Product, user: User, rating: int):
    product_rating = ProductRating(rating)
    product_rating.product_id = product.id
    product_rating.user_id = user.id
    session.add(product_rating)
    session.commit()


def get_ratings(product: Product):
    return ProductRating.query.filter_by(product_id=product.id).all()


def get_product_rating_by_user(product: Product, user: User):
    return ProductRating.query.filter_by(product_id=product.id, user_id=user.id).first()


def delete_rating(product: Product, user: User):
    session.delete(ProductRating.query.filter_by(product_id=product.id, user_id=user.id).first())
    session.commit()


def update(product, attributes: set, data):
    sorted_attributes = sorted(attributes)
    for attribute in sorted_attributes:
        if data.get(attribute) is not None and hasattr(product, attribute):
            try:
                setattr(product, attribute, data[attribute])
            except (TypeError, ValueError) as e:
                session.rollback()
                raise e

    session.commit()
