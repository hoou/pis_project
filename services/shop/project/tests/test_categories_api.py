import json

from flask_api import status
from flask_jwt_extended import create_access_token

from project.business import categories, users
from project.models.user import UserRole


def test_get_all_categories(client):
    categories.add(name='Men')
    categories.add(name='Women')
    categories.add(name='Kids')
    categories.add(name='Shirts')

    r = client.get('/api/categories/')

    payload = r.json

    all_categories = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(all_categories) == 4

    sorted_categories = sorted(all_categories, key=lambda category: category['id'])

    assert sorted_categories[0]['name'] == 'Men'
    assert sorted_categories[1]['name'] == 'Women'
    assert sorted_categories[2]['name'] == 'Kids'
    assert sorted_categories[3]['name'] == 'Shirts'


def test_add_category(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

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

    r = client.post(
        '/api/categories/',
        data=json.dumps({
            'name': 'Men'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Category was successfully added.'


def test_add_category_empty_json(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

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

    r = client.post(
        '/api/categories/',
        data=json.dumps({}),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_category_not_existing_user(client):
    not_existing_user_id = 99
    access_token = create_access_token(not_existing_user_id)

    r = client.post(
        '/api/categories/',
        data=json.dumps({
            'name': 'Men'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Incorrect authentication credentials.'


def test_add_category_not_active_user(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.role = UserRole.ADMIN

    access_token = create_access_token(user.id)

    r = client.post(
        '/api/categories/',
        data=json.dumps({
            'name': 'Men'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_category_not_logged_in(client):
    r = client.post(
        '/api/categories/',
        data=json.dumps({
            'name': 'Men'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_category_not_admin_or_worker(client):
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

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.post(
        '/api/categories/',
        data=json.dumps({
            'name': 'Men'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_delete_category(client):
    category = categories.add(name='Men')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert category.id

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

    r = client.delete(f'/api/categories/{category.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Category was successfully deleted.'
    assert categories.get(category.id) is None


def test_delete_not_existing_category(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

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

    not_existing_category_id = 99

    r = client.delete(
        f'/api/categories/{not_existing_category_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Category not found.'


def test_delete_category_no_admin_or_worker(client):
    category = categories.add(name='Men')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    assert category.id
    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

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

    r = client.delete(f'/api/categories/{category.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_delete_category_not_logged_in(client):
    category = categories.add(name='Men')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert category.id

    r = client.delete(f'/api/categories/{category.id}')
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_category(client):
    category = categories.add(name='Mans')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

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

    assert category.name == 'Mans'

    r = client.put(
        f'/api/categories/{category.id}',
        data=json.dumps({
            'name': 'Men'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Category was successfully modified.'
    assert category.name == 'Men'


def test_update_category_empty_json(client):
    category = categories.add(name='Mans')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

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

    assert category.name == 'Mans'

    r = client.put(
        f'/api/categories/{category.id}',
        data=json.dumps({}),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_not_existing_category(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

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

    not_existing_category_id = 99

    r = client.put(
        f'/api/categories/{not_existing_category_id}',
        data=json.dumps({
            'name': 'Men'
        }),
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Category not found.'


def test_update_category_no_admin_or_worker(client):
    category = categories.add(name='Mans')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    assert category.id
    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

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

    r = client.put(f'/api/categories/{category.id}',
                   data=json.dumps({
                       'name': 'Men'
                   }),
                   headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_category_not_logged_in(client):
    category = categories.add(name='Mans')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert category.id

    r = client.put(
        f'/api/categories/{category.id}',
        data=json.dumps({
            'name': 'Men'
        })
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'
