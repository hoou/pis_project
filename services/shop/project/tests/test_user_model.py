import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from project.api.models import User


def test_add_user(app, db_session: Session):
    user = User('tibor@mikita.eu', 'halo')
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email == 'tibor@mikita.eu'
    assert user.password == 'halo'


def test_add_user_duplicate_email(app, db_session: Session):
    user = User('tibor@mikita.eu', 'halo')
    user2 = User('tibor@mikita.eu', 'blah')

    db_session.add(user)
    db_session.commit()

    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()

