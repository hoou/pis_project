from sqlalchemy.orm import Session

from project import db
from project.models.product import Product
from project.models.product_image import ProductImage

session: Session = db.session


def add(**kwargs):
    product = Product(**kwargs)

    session.add(product)

    session.commit()

    return product


def get_all():
    return Product.query.filter_by(is_deleted=False).all()


def get(product_id):
    return Product.query.filter_by(id=product_id, is_deleted=False).first()


def delete(product: Product):
    product.is_deleted = True
    session.commit()


def add_image(product: Product, **kwargs):
    image = ProductImage(**kwargs)
    image.product_id = product.id
    product.images += [image]
    return image


def get_images(product_id):
    return ProductImage.query.filter_by(product_id=product_id).all()


def delete_image(image_id):
    session.delete(ProductImage.query.filter_by(id=image_id).first())


def has_image(product_id, image_id):
    product_images = get_images(product_id)
    image = ProductImage.query.filter_by(id=image_id).first()
    return image in product_images
