import json

import os
from flask_api import status
from flask_jwt_extended import create_access_token

from project.models.product_image import ProductImage
from project.models.user import UserRole
from project.business import products, users

basedir = os.path.abspath(os.path.dirname(__file__))
product_dir = os.path.join(basedir, )
testing_image_jpg_path = os.path.join(basedir, 'test_files/lena.jpg')
testing_image_png_path = os.path.join(basedir, 'test_files/lena.png')


def test_get_all_products(client):
    products.add(name='Product One', price=13.99)
    products.add(name='Product Two', price=23.99, description='blah')
    products.add(name='Product Three', price=3.99)
    products.add(name='Product Four', price=68.99)

    r = client.get('/api/products/')

    payload = r.json

    all_products = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(all_products) == 4

    sorted_products = sorted(all_products, key=lambda product: product['id'])

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
    product = products.add(name='Super Product', price=99.99)

    r = client.get(f'/api/products/{product.id}')

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['name'] == 'Super Product'
    assert payload['price'] == 99.99
    assert payload['description'] is None


def test_get_single_product_non_existing(client):
    non_existing_product_id = 999

    r = client.get(f'/api/products/{non_existing_product_id}')

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert 'Product not found.' in payload['message']


def test_add_product(app, client):
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
        '/api/products/',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Product was successfully added.'


def test_add_product_empty_json(client):
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
        '/api/products/',
        data=json.dumps({}),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_not_existing_user(client):
    not_existing_user_id = 99
    access_token = create_access_token(not_existing_user_id)

    r = client.post(
        '/api/products/',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Incorrect authentication credentials.'


def test_add_product_not_active_user(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.role = UserRole.ADMIN

    access_token = create_access_token(user.id)

    r = client.post(
        '/api/products/',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_not_logged_in(client):
    r = client.post(
        '/api/products/',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_not_admin_or_worker(client):
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
        '/api/products/',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_missing_name(client):
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
        '/api/products/',
        data=json.dumps({
            'price': 213.212,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_missing_price(client):
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
        '/api/products/',
        data=json.dumps({
            'name': 'Super Perfect Product Numero Uno',
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_delete_product(client):
    product = products.add(name='Super Small Product', price=0.99)

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

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

    r = client.delete(f'/api/products/{product.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Product was successfully deleted.'
    assert products.get(product.id) is None


def test_delete_not_existing_product(client):
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

    not_existing_product_id = 99

    r = client.delete(
        f'/api/products/{not_existing_product_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_delete_product_no_admin_or_worker(client):
    product = products.add(name='Super Small Product', price=0.99)

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    assert product.id
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

    r = client.delete(f'/api/products/{product.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_delete_product_not_logged_in(client):
    product = products.add(name='Super Small Product', price=0.99)

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

    r = client.delete(f'/api/products/{product.id}')
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_image(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={
                'file': (f, f.name)
            },
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Image was successfully uploaded.'
    assert len(product.images) == 1
    assert isinstance(product.images[0], ProductImage)
    assert product.images[0].url


def test_add_product_image_not_existing_product(client):
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

    not_existing_product_id = 99

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{not_existing_product_id}/images',
            data={
                'file': (f, f.name)
            },
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_add_product_image_no_data(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_image_not_admin_or_worker(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    assert user.role != UserRole.WORKER and user.role != UserRole.ADMIN

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={
                'file': (f, f.name)
            },
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_image_no_file(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={},
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_image_empty_file(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={
                'file': None
            },
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_image_not_file(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={
                'file': 'blah'
            },
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_image_not_logged_in(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

    with open(testing_image_jpg_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={
                'file': (f, f.name)
            },
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_image_not_allowed_file_ext(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    product = products.add(name='Super Small Product', price=0.99)

    assert product.id

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

    with open(testing_image_png_path, 'rb') as f:
        r = client.post(
            f'/api/products/{product.id}/images',
            data={
                'file': (f, f.name)
            },
            headers={'Authorization': f'Bearer {access_token}'},
            content_type='multipart/form-data'
        )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'File extension not allowed.'


def test_get_images_of_product(client):
    product = products.add(name='Super Small Product', price=0.99)
    products.add_image(product, url='fake_url.jpg')
    products.add_image(product, url='fake_url2.jpg')
    products.add_image(product, url='fake_url3.jpg')

    r = client.get(f'/api/products/{product.id}/images')
    payload = r.json

    assert r.status_code == status.HTTP_200_OK

    images = payload

    assert len(images) == 3

    for image in images:
        assert 'fake_url' in image['url']


def test_delete_image_of_product(client):
    product = products.add(name='Super Small Product', price=0.99)
    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

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

    r = client.delete(f'/api/products/{product.id}/images/{image.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Image was successfully deleted.'


def test_delete_image_of_different_product(client):
    product = products.add(name='Super Small Product', price=0.99)
    product_without_image = products.add(name='Different Product', price=2.99)
    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

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

    r = client.delete(
        f'/api/products/{product_without_image.id}/images/{image.id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Image not found.'


def test_delete_image_not_existing(client):
    product = products.add(name='Super Small Product', price=0.99)

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

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

    not_existing_image_id = 99

    r = client.delete(
        f'/api/products/{product.id}/images/{not_existing_image_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Image not found.'


def test_delete_image_of_product_no_admin_or_worker(client):
    product = products.add(name='Super Small Product', price=0.99)
    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    assert product.id
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

    r = client.delete(f'/api/products/{product.id}/images/{image.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_delete_image_of_product_not_logged_in(client):
    product = products.add(name='Super Small Product', price=0.99)
    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

    r = client.delete(f'/api/products/{product.id}/images/{image.id}')
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'
