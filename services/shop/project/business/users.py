from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project import db
from project.models.user import User

session: Session = db.session


class DuplicateEmailError(Exception):
    pass


def add(user: User):
    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        raise DuplicateEmailError('Sorry. User with that email already exists.')

    return user


def get(user_id: int) -> User:
    return User.query.filter_by(_id=user_id).first()


def get_by_email(email):
    return User.query.filter_by(_email=email).first()


def get_all():
    return User.query.all()


def update(user, attributes: set, data):
    session.begin_nested()

    sorted_attributes = sorted(attributes)
    for attribute in sorted_attributes:
        if data.get(attribute) is not None and hasattr(user, attribute):
            try:
                setattr(user, attribute, data[attribute])
            except (TypeError, ValueError) as e:
                session.rollback()
                raise e

    session.commit()
