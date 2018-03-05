from project.models.user import User
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


def test_add_user(app, db_session: Session):
    user = User('tibor@mikita.eu', 'halo')
    db_session.add(user)
    db_session.commit()

    assert user.id
    assert user.email == 'tibor@mikita.eu'
    assert user.password


def test_add_user_duplicate_email(app, db_session: Session):
    user = User('tibor@mikita.eu', 'halo')
    user2 = User('tibor@mikita.eu', 'blah')

    db_session.add(user)
    db_session.commit()

    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_passwords_are_random(app, db_session: Session):
    user1 = User('user1@server.eu', 'blah')
    user2 = User('user2@server.eu', 'blah')

    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    assert user1.password != user2.password


def test_encode_auth_token(app, db_session: Session):
    user = User('tibor@mikita.eu', 'blah')
    db_session.add(user)
    db_session.commit()

    auth_token = user.encode_auth_token()
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(app, db_session: Session):
    user = User('tibor@mikita.eu', 'blah')
    db_session.add(user)
    db_session.commit()

    auth_token = user.encode_auth_token()

    decoded_token = User.decode_auth_token(auth_token)

    assert decoded_token == user.id


def test_decode_expired_auth_token(app, db_session: Session):
    user = User('tibor@mikita.eu', 'blah')
    db_session.add(user)
    db_session.commit()

    auth_token = user.encode_auth_token()

    import time
    time.sleep(app.config.get('TOKEN_EXPIRATION_SECONDS') + 1)

    decoded_token = User.decode_auth_token(auth_token)

    assert decoded_token == 'Signature expired. Please log in again.'


def test_decode_invalid_auth_token(app, db_session: Session):
    decoded_token = User.decode_auth_token("blablabla")

    assert decoded_token == 'Invalid token. Please log in again.'
