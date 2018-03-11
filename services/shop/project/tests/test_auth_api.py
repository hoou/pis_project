import json

import datetime
from flask_api import status

from project.business import users


def test_user_registration(client):
    r = client.post(
        '/api/auth/register',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )
    payload = r.json
    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Successfully registered.'


def test_user_registration_duplicate_email(client):
    users.add(email='tibor@mikita.eu', password='halo')

    r = client.post(
        '/api/auth/register',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_409_CONFLICT
    assert payload['message'] == 'User with this email already exists.'


def test_user_registration_empty_json(client):
    r = client.post(
        '/api/auth/register',
        data=json.dumps({}),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_user_registration_no_password(client):
    r = client.post(
        '/api/auth/register',
        data=json.dumps({
            'email': 'tibor@mikita.eu'
        }),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_user_registration_no_email(client):
    r = client.post(
        '/api/auth/register',
        data=json.dumps({
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_user_login(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'User successfully logged in.'
    assert payload['access_token']


def test_user_login_inactive(client):
    user = users.add(email='tibor@mikita.eu', password='blah')

    assert not user.active

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_user_login_empty_json(client):
    r = client.post(
        '/api/auth/login',
        data=json.dumps({}),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_user_login_missing_password(client):
    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_user_login_missing_email(client):
    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_user_login_not_registered(client):
    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Incorrect authentication credentials.'


def test_user_login_invalid_password(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah-blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Incorrect authentication credentials.'


def test_user_logout(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )
    payload = r.json

    access_token = payload['access_token']

    r = client.get(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'User successfully logged out.'


def test_user_logout_no_header(client):
    r = client.get(
        '/api/auth/logout'
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_user_logout_no_token(client):
    r = client.get(
        '/api/auth/logout',
        headers={'Authorization': 'Bearer'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Malformed request.'


def test_user_logout_empty_auth_header(client):
    r = client.get(
        '/api/auth/logout',
        headers={'Authorization': ''}
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_user_logout_invalid_token(client):
    r = client.get(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer hi_im_invalid_token_nice_to_meet_you'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Malformed request.'


def test_user_logout_expired_token(app, client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=-1)

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )
    payload = r.json

    access_token = payload['access_token']

    r = client.get(
        '/api/auth/logout',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Expired access token.'
