import datetime
import json

from flask_api import status
from flask_jwt_extended import decode_token

from project.business import users
from project.models.user import User, UserRole


def test_status(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.WORKER

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
        '/api/auth/status',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['role'] == 'worker'
    assert payload['email'] == 'tibor@mikita.eu'


def test_status_not_logged_in(client):
    r = client.get('/api/auth/status', )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_status_not_active(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.role = UserRole.ADMIN
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

    user.active = False

    assert user.active is False

    r = client.get(
        '/api/auth/status',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You have not active account.'


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
    users.add(User(email='tibor@mikita.eu', password='blah'))

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    assert payload['access_token']
    assert payload['refresh_token']


def test_user_login_inactive(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))

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
    assert payload['message'] == 'You have not active account.'


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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    assert payload['message'] == 'Expired token.'


def test_refresh_token(app, client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=1)

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
    refresh_token = payload['refresh_token']

    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3)

    r = client.get(
        '/api/auth/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )

    payload = r.json

    old_access_token = access_token

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Token successfully refreshed.'
    assert payload['access_token']

    decoded_access_token = decode_token(payload['access_token'])
    decoded_old_access_token = decode_token(old_access_token)

    assert decoded_access_token['exp'] > decoded_old_access_token['exp']
    assert decoded_access_token['identity'] == decoded_old_access_token['identity']


def test_refresh_token_with_access_token(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
        '/api/auth/refresh',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Wrong type of token given.'


def test_refresh_token_with_expired_token(app, client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True

    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(seconds=-1)

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    refresh_token = payload['refresh_token']

    r = client.get(
        '/api/auth/refresh',
        headers={'Authorization': f'Bearer {refresh_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Expired token.'


def test_refresh_token_with_no_refresh_token(client):
    r = client.get(
        '/api/auth/refresh',
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_refresh_token_with_empty_token(client):
    r = client.get(
        '/api/auth/refresh',
        headers={'Authorization': ''}
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_refresh_token_with_invalid_token(client):
    r = client.get(
        '/api/auth/refresh',
        headers={'Authorization': 'Bearer blabla_invalid_token'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Malformed request.'
