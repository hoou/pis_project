import jwt
import pytest

from project.store import user_store
from project.utils.jwt import encode_auth_token
from project.utils.jwt import decode_auth_token


def test_add_user(app):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    assert user.id
    assert user.email == 'tibor@mikita.eu'
    assert user.password


def test_add_user_duplicate_email(app):
    user_store.add(email='tibor@mikita.eu', password='halo')

    from project.store.user_store import DuplicateEmailError
    with pytest.raises(DuplicateEmailError):
        user_store.add(email='tibor@mikita.eu', password='blah')


def test_passwords_are_random(app):
    user1 = user_store.add(email='user1@server.eu', password='blah')
    user2 = user_store.add(email='user2@server.eu', password='blah')

    assert user1.password != user2.password


def test_encode_auth_token(app):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    auth_token = encode_auth_token(user.id)
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(app):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    auth_token = encode_auth_token(user.id)

    decoded_token = decode_auth_token(auth_token)

    assert decoded_token == user.id


def test_decode_expired_auth_token(app):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    auth_token = encode_auth_token(user.id)

    import time
    time.sleep(app.config.get('TOKEN_EXPIRATION_SECONDS') + 1)

    with pytest.raises(jwt.ExpiredSignatureError):
        decode_auth_token(auth_token)


def test_decode_invalid_auth_token(app):
    with pytest.raises(jwt.InvalidTokenError):
        decode_auth_token("blablabla")
