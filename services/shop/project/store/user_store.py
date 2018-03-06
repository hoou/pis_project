from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project import db
from project.models.user import User, UserRole

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


def get_by_email(email):
    return User.query.filter_by(email=email).first()


def get_all():
    return User.query.all()


def set_active(user_id: int):
    User.query.filter_by(id=user_id).first().active = True


def set_admin(user_id: int):
    User.query.filter_by(id=user_id).first().role = UserRole.ADMIN


def set_worker(user_id: int):
    User.query.filter_by(id=user_id).first().role = UserRole.WORKER
