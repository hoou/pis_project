import json

from flask_api import status

from project.models.user import UserRole
from project.store import user_store


def test_get_single_user_as_admin(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')
    user.active = True
    user.role = UserRole.ADMIN

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        f'/api/users/{user.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json

    user = payload

    assert r.status_code == status.HTTP_200_OK
    assert user['email'] == 'tibor@mikita.eu'


def test_get_single_user_as_worker(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')
    user.active = True
    user.role = UserRole.ADMIN

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        f'/api/users/{user.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json

    user = payload

    assert r.status_code == status.HTTP_200_OK
    assert user['email'] == 'tibor@mikita.eu'


def test_get_single_user_not_admin_or_worker(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')
    user.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.get(
        f'/api/users/{user.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_single_user_not_logged_in(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    r = client.get(
        f'/api/users/{user.id}'
    )

    payload = r.json
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_single_user_not_exist(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')
    user.active = True
    user.role = UserRole.ADMIN

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    non_existing_id = 999
    r = client.get(
        f'/api/users/{non_existing_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert 'This resource does not exist.' in payload['message']


def test_get_all_users_as_admin(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    user = user_store.get_by_email('user1@server.eu')
    user.active = True
    user.role = UserRole.ADMIN

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'user1@server.eu',
            'password': 'pass1'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        '/api/users/',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    users = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(users) == number_of_users

    # sort by id
    sorted_users = sorted(users, key=lambda x: x['id'])

    for i, user in enumerate(sorted_users):
        assert user['email'] == f'user{i}@server.eu'


def test_get_all_users_as_worker(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    user = user_store.get_by_email('user1@server.eu')
    user.active = True
    user.role = UserRole.ADMIN

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'user1@server.eu',
            'password': 'pass1'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        '/api/users/',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json

    users = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(users) == number_of_users

    # sort by id
    sorted_users = sorted(users, key=lambda x: x['id'])

    for i, user in enumerate(sorted_users):
        assert user['email'] == f'user{i}@server.eu'


def test_get_all_users_not_admin_or_worker(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    user = user_store.get_by_email('user1@server.eu')
    user.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'user1@server.eu',
            'password': 'pass1'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.get(
        '/api/users/',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_all_users_not_logged_in(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    r = client.get(
        '/api/users/'
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'
