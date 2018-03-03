import json

from flask_api import status
from project.api.models import User
from sqlalchemy.orm import Session


def test_ping(client):
    r = client.get('/users/ping')
    payload = r.json
    assert r.status_code == status.HTTP_200_OK
    assert 'pong!' in payload['message']
    assert 'success' in payload['status']


def test_add_user(client):
    r = client.post(
        '/users',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json'
    )
    payload = r.json
    assert r.status_code == status.HTTP_201_CREATED
    assert 'success' in payload['status']
    assert 'User was added.' in payload['message']


def test_add_user_invalid_json(client):
    r = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json'
    )
    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Invalid payload.' == payload['message']
    assert 'fail' in payload['status']


def test_add_user_invalid_json_keys(client):
    r = client.post(
        '/users',
        data=json.dumps({'email': 'tibor@mikita.eu'}),
        content_type='application/json',
    )
    payload = r.json
    assert r.status_code == 400
    assert 'Invalid payload.' in payload['message']
    assert 'fail' in payload['status']


def test_add_user_duplicate_email(client):
    client.post(
        '/users',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json',
    )
    r = client.post(
        '/users',
        data=json.dumps({
            'email': 'tibor@mikita.eu',
            'password': 'halo'
        }),
        content_type='application/json',
    )
    payload = r.json
    assert r.status_code == status.HTTP_409_CONFLICT
    assert 'Sorry. User with that email already exists.' == payload['message']
    assert 'fail' == payload['status']


def test_get_single_user(client, db_session: Session):
    user = User('tibor@mikita.eu', 'halo')
    db_session.add(user)
    db_session.commit()
    r = client.get(f'/users/{user.id}')
    payload = r.json
    assert r.status_code == status.HTTP_200_OK
    assert 'tibor@mikita.eu' in payload['data']['email']
    assert 'success' in payload['status']


def test_get_single_user_not_exist(client):
    non_existing_id = 999
    r = client.get(f'/users/{non_existing_id}')
    payload = r.json
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert 'fail' in payload['status']
    assert 'User not found.' in payload['message']


def test_get_single_user_id_not_int(client):
    non_int_id = 'blah'
    r = client.get(f'/users/{non_int_id}')
    payload = r.json
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'fail' in payload['status']
    assert 'Bad request.' in payload['message']


def test_get_all_users(client, db_session: Session):
    number_of_users = 3

    for i in range(number_of_users):
        db_session.add(User(f'user{i}@server.eu', f'pass{i}'))
    db_session.commit()

    r = client.get('/users')
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert 'success' in payload['status']
    assert len(payload['data']) == number_of_users
    for i in range(number_of_users):
        assert f'user{i}@server.eu' in payload['data'][i]['email']
        assert f'pass{i}' in payload['data'][i]['password']
