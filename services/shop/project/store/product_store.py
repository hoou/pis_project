from sqlalchemy.orm import Session

from project import db
from project.models.product import Product
from project.models.product_image import ProductImage

session: Session = db.session


def add(**kwargs):
    product = Product(**kwargs)

    session.add(product)

    session.commit()

    # try:
    #     pass
    # except IntegrityError:
    #     session.rollback()
    #     raise DuplicateEmailError('Sorry. User with that email already exists.')

    return product


def get_all():
    return Product.query.all()


def get(product_id):
    return Product.query.filter_by(id=product_id).first()


def add_image(product: Product, **kwargs):
    image = ProductImage(**kwargs)
    image.product_id = product.id
    product.images += [image]
