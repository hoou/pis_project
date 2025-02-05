from sqlalchemy.orm import Session

from project import db
from project.models.category import Category
from project.models.product import Product

session: Session = db.session


def add(category: Category):
    session.add(category)
    session.commit()
    return category


def get_all():
    return Category.query.all()


def get(category_id):
    return Category.query.filter_by(id=category_id).first()


def delete(category_id):
    category = get(category_id)
    session.delete(category)
    session.commit()


def add_product(category: Category, product: Product):
    category.products.append(product)
    session.commit()


def change_name(category: Category, name: str):
    category.name = name
    session.commit()
