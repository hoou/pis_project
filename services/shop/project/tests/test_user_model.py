import jwt
import pytest

from project.store import user_store


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

    auth_token = user.encode_auth_token()
    assert isinstance(auth_token, bytes)


def test_decode_auth_token(app):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    auth_token = user.encode_auth_token()

    from project.models.user import User  # FIXME remove this
    decoded_token = User.decode_auth_token(auth_token)

    assert decoded_token == user.id


def test_decode_expired_auth_token(app):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    auth_token = user.encode_auth_token()

    import time
    time.sleep(app.config.get('TOKEN_EXPIRATION_SECONDS') + 1)

    from project.models.user import User  # FIXME remove this
    with pytest.raises(jwt.ExpiredSignatureError):
        User.decode_auth_token(auth_token)


def test_decode_invalid_auth_token(app):
    from project.models.user import User  # FIXME remove this
    with pytest.raises(jwt.InvalidTokenError):
        User.decode_auth_token("blablabla")
