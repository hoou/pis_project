from sqlalchemy.orm import Session

from project import db
from project.models.category import Category

session: Session = db.session


def add(**kwargs):
    category = Category(**kwargs)
    session.add(category)
    session.commit()
    return category


def get_all():
    return Category.query.all()


def get(category_id):
    return Category.query.filter_by(id=category_id).first()


def remove(category_id):
    category = get(category_id)
    session.delete(category)
    session.commit()
