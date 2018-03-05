from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project import db
from project.models.user import User

session: Session = db.session


class DuplicateEmailError(Exception):
    pass


def add(**kwargs):
    user = User(**kwargs)

    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise DuplicateEmailError('Sorry. User with that email already exists.')

    return user


def get(user_id: int):
    return User.query.filter_by(id=user_id).first()


def get_all():
    return User.query.all()
