import json

from flask_api import status

from project.models.user import UserRole
from project.store import product_store, user_store
from project.utils.jwt import encode_auth_token


def test_get_all_products(client):
    product_store.add(name='Product One', price=13.99)
    product_store.add(name='Product Two', price=23.99, description='blah')
    product_store.add(name='Product Three', price=3.99)
    product_store.add(name='Product Four', price=68.99)

    r = client.get('/products')

    payload = r.json
    products = payload['data']

    assert r.status_code == status.HTTP_200_OK
    assert payload['status'] == 'success'
    assert len(products) == 4

    sorted_products = sorted(products, key=lambda product: product['id'])

    assert sorted_products[0]['name'] == 'Product One'
    assert sorted_products[1]['name'] == 'Product Two'
    assert sorted_products[2]['name'] == 'Product Three'
    assert sorted_products[3]['name'] == 'Product Four'

    assert sorted_products[0]['price'] == 13.99
    assert sorted_products[1]['price'] == 23.99
    assert sorted_products[2]['price'] == 3.99
    assert sorted_products[3]['price'] == 68.99

    assert sorted_products[0]['description'] is None
    assert sorted_products[1]['description'] == 'blah'
    assert sorted_products[2]['description'] is None
    assert sorted_products[3]['description'] is None


def test_get_single_product(client):
    product = product_store.add(name='Super Product', price=99.99)

    r = client.get(f'/products/{product.id}')

    payload = r.json
    data = payload['data']

    assert r.status_code == status.HTTP_200_OK
    assert payload['status'] == 'success'
    assert data['name'] == 'Super Product'
    assert data['price'] == 99.99
    assert data['description'] is None


def test_get_single_product_non_existing(client):
    non_existing_product_id = 999

    r = client.get(f'/products/{non_existing_product_id}')

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Product not found.'


def test_add_product(client):
    admin = user_store.add(email='tibor@mikita.eu', password='blah')
    user_store.set_active(admin.id)
    user_store.set_admin(admin.id)

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

    r = client.post(
        '/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['status'] == 'success'
    assert payload['message'] == 'Product was successfully added.'


def test_add_product_empty_json(client):
    admin = user_store.add(email='tibor@mikita.eu', password='blah')
    user_store.set_active(admin.id)
    user_store.set_admin(admin.id)

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

    r = client.post(
        '/products',
        data=json.dumps({}),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_add_product_not_existing_user(client):
    not_existing_user_id = 99
    auth_token = encode_auth_token(not_existing_user_id).decode()

    r = client.post(
        '/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid user id.'


def test_add_product_not_active_user(client):
    admin = user_store.add(email='tibor@mikita.eu', password='blah')
    user_store.set_admin(admin.id)

    auth_token = encode_auth_token(admin.id).decode()

    r = client.post(
        '/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'User is not active.'


def test_add_product_not_logged_in(client):
    r = client.post(
        '/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Authorization header missing.'


def test_add_product_not_admin_or_worker(client):
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

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.post(
        '/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['status'] == 'fail'
    assert payload['message'] == 'You do not have permission to do that.'


def test_add_product_missing_name(client):
    admin = user_store.add(email='tibor@mikita.eu', password='blah')
    user_store.set_active(admin.id)
    user_store.set_admin(admin.id)

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

    r = client.post(
        '/products',
        data=json.dumps({
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'


def test_add_product_missing_price(client):
    admin = user_store.add(email='tibor@mikita.eu', password='blah')
    user_store.set_active(admin.id)
    user_store.set_admin(admin.id)

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

    r = client.post(
        '/products',
        data=json.dumps({
            'name': 'Super Perfect Product Numero Uno',
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {auth_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['status'] == 'fail'
    assert payload['message'] == 'Invalid payload.'
