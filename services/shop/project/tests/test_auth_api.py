import json

import time
from flask_api import status

from project.store import user_store


def test_user_registration(client):
    r = client.post(
        '/auth/register',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )
    payload = r.json
    assert r.status_code == status.HTTP_201_CREATED
    assert payload['status'] == 'success'
    assert payload['message'] == 'Successfully registered.'


def test_user_registration_duplicate_email(client):
    user_store.add(email='tibor@mikita.eu', password='halo')

    r = client.post(
        '/auth/register',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_409_CONFLICT
    assert payload['status'] == 'fail'
    assert payload['message'] == 'User with this email already exists.'


def test_user_registration_empty_json(client):
    r = client.post(
        '/auth/register',
        data=json.dumps({}),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_user_registration_no_password(client):
    r = client.post(
        '/auth/register',
        data=json.dumps({
            'email': 'tibor@mikita.eu'
        }),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_user_registration_no_email(client):
    r = client.post(
        '/auth/register',
        data=json.dumps({
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_user_login(client):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    user_store.set_active(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['status'] == 'success'
    assert payload['message'] == 'User successfully logged in.'
    assert payload['auth_token']


def test_user_login_inactive(client):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    assert not user.active

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'User is not active.'


def test_user_login_empty_json(client):
    r = client.post(
        '/auth/login',
        data=json.dumps({}),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_user_login_missing_password(client):
    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_user_login_missing_email(client):
    r = client.post(
        '/auth/login',
        data=json.dumps({
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_user_login_not_registered(client):
    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['status'] == 'fail'
    assert payload['message'] == 'User with this email is not registered.'


def test_user_login_invalid_password(client):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    user_store.set_active(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah-blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid password.'


def test_user_logout(client):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    user_store.set_active(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )
    payload = r.json

    auth_token = payload['auth_token']

    r = client.get(
        '/auth/logout',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['status'] == 'success'
    assert payload['message'] == 'User successfully logged out.'


def test_user_logout_no_header(client):
    r = client.get(
        '/auth/logout'
    )
    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Authorization header missing.'


def test_user_logout_no_token(client):
    r = client.get(
        '/auth/logout',
        headers={'Authorization': 'Bearer'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid authorization header.'


def test_user_logout_empty_auth_header(client):
    r = client.get(
        '/auth/logout',
        headers={'Authorization': ''}
    )
    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid authorization header.'


def test_user_logout_invalid_token(client):
    r = client.get(
        '/auth/logout',
        headers={'Authorization': f'Bearer hi_im_invalid_token_nice_to_meet_you'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid token.'


def test_user_logout_expired_token(app, client):
    user = user_store.add(email='tibor@mikita.eu', password='blah')

    user_store.set_active(user.id)

    app.config['TOKEN_EXPIRATION_SECONDS'] = -1

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )
    payload = r.json

    auth_token = payload['auth_token']

    r = client.get(
        '/auth/logout',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Expired token.'
