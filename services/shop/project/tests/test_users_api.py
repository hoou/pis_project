import json

from flask_api import status

from project.models.user import UserRole
from project.store import user_store


def test_get_single_user_as_admin(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    user_store.set_active(user.id)
    user_store.set_admin(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json
    assert r.status_code == status.HTTP_200_OK
    assert payload['data']['email'] == 'tibor@mikita.eu'
    assert payload['status'] == 'success'


def test_get_single_user_as_worker(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    user_store.set_active(user.id)
    user_store.set_worker(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json
    assert r.status_code == status.HTTP_200_OK
    assert payload['data']['email'] == 'tibor@mikita.eu'
    assert payload['status'] == 'success'


def test_get_single_user_not_admin_or_worker(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    user_store.set_active(user.id)

    r = client.post(
        '/auth/login',
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
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'You do not have permission to do that.'


def test_get_single_user_not_logged_in(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    r = client.get(
        f'/users/{user.id}'
    )

    payload = r.json
    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'You do not have permission to do that.'


def test_get_single_user_not_exist(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    user_store.set_active(user.id)
    user_store.set_admin(user.id)

    r = client.post(
        '/auth/login',
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
        f'/users/{non_existing_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['status'] == 'fail'
    assert payload['message'] == 'User not found.'


def test_get_single_user_id_not_int(client):
    user = user_store.add(email='tibor@mikita.eu', password='halo')

    user_store.set_active(user.id)
    user_store.set_admin(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    non_int_id = 'blah'
    r = client.get(
        f'/users/{non_int_id}',
        headers={'Authorization': f'Bearer {auth_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'User id must be int.'


def test_get_all_users_as_admin(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    user = user_store.get_by_email('user1@server.eu')
    user_store.set_active(user.id)
    user_store.set_admin(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'user1@server.eu',
            'password': 'pass1'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        '/users',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['status'] == 'success'
    assert len(payload['data']) == number_of_users

    # sort by id
    sorted_users = sorted(payload['data'], key=lambda x: x['id'])

    for i, user in enumerate(sorted_users):
        assert user['email'] == f'user{i}@server.eu'
        assert user['password']


def test_get_all_users_as_worker(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    user = user_store.get_by_email('user1@server.eu')
    user_store.set_active(user.id)
    user_store.set_worker(user.id)

    r = client.post(
        '/auth/login',
        data=json.dumps({
            'email': 'user1@server.eu',
            'password': 'pass1'
        }),
        content_type='application/json'
    )

    payload = r.json
    auth_token = payload['auth_token']

    r = client.get(
        '/users',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['status'] == 'success'
    assert len(payload['data']) == number_of_users

    # sort by id
    sorted_users = sorted(payload['data'], key=lambda x: x['id'])

    for i, user in enumerate(sorted_users):
        assert user['email'] == f'user{i}@server.eu'
        assert user['password']


def test_get_all_users_not_admin_or_worker(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    user = user_store.get_by_email('user1@server.eu')
    user_store.set_active(user.id)

    r = client.post(
        '/auth/login',
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
        '/users',
        headers={'Authorization': f'Bearer {auth_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'You do not have permission to do that.'


def test_get_all_users_not_logged_in(client):
    number_of_users = 3

    for i in range(number_of_users):
        user_store.add(email=f'user{i}@server.eu', password=f'pass{i}')

    r = client.get(
        '/users'
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'You do not have permission to do that.'
