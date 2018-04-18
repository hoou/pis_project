import json

import os
from flask_api import status
from flask_jwt_extended import create_access_token

from project.models.category import Category
from project.models.product import Product
from project.models.product_image import ProductImage
from project.models.user import UserRole, User
from project.business import products, users, categories

basedir = os.path.abspath(os.path.dirname(__file__))
product_dir = os.path.join(basedir, )
testing_image_jpg_path = os.path.join(basedir, 'test_files/lena.jpg')
testing_image_png_path = os.path.join(basedir, 'test_files/lena.png')


def test_get_all_products(client):
    category = categories.add(Category(name='Men'))
    categories.add_product(category, Product(name='Product One', price=13.99))
    product = Product(name='Product Two', price=23.99, description='blah')
    categories.add_product(category, product)
    categories.add_product(category, Product(name='Product Three', price=3.99, count=5))
    categories.add_product(category, Product(name='Product Four', price=68.99))
    products.delete(product)

    r = client.get('/api/products/')

    payload = r.json

    all_products = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(all_products) == 3

    sorted_products = sorted(all_products, key=lambda product_: product_['id'])

    assert sorted_products[0]['name'] == 'Product One'
    assert sorted_products[1]['name'] == 'Product Three'
    assert sorted_products[2]['name'] == 'Product Four'

    assert sorted_products[0]['price'] == 13.99
    assert sorted_products[1]['price'] == 3.99
    assert sorted_products[2]['price'] == 68.99

    assert sorted_products[0]['count'] == 0
    assert sorted_products[1]['count'] == 5
    assert sorted_products[2]['count'] == 0

    assert sorted_products[0]['description'] is None
    assert sorted_products[1]['description'] is None
    assert sorted_products[2]['description'] is None

    assert sorted_products[0]['category']['name'] == \
           sorted_products[1]['category']['name'] == \
           sorted_products[2]['category']['name'] == \
           'Men'


def test_get_single_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Product', price=99.99, count=5)
    categories.add_product(category, product)

    r = client.get(f'/api/products/{product.id}')

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['name'] == 'Super Product'
    assert payload['price'] == 99.99
    assert payload['count'] == 5
    assert payload['description'] is None


def test_get_single_already_deleted_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Product', price=99.99)
    categories.add_product(category, product)
    products.delete(product)

    assert product.is_deleted

    r = client.get(f'/api/products/{product.id}')

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_get_single_product_non_existing(client):
    non_existing_product_id = 999

    r = client.get(f'/api/products/{non_existing_product_id}')

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert 'Product not found.' in payload['message']


def test_add_product(client):
    category = categories.add(Category(name='Men'))

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah',
            'count': 5
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Product was successfully added.'

    product = products.get_all()[0]

    assert product.name == 'New Super Product'
    assert product.price == 213.99
    assert product.description == 'blah blah blah'
    assert product.count == 5


def test_add_product_not_existing_category(client):
    not_existing_category_id = 99

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
        f'/api/categories/{not_existing_category_id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Category not found.'


def test_add_product_empty_json(client):
    category = categories.add(Category(name='Men'))

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
        f'/api/categories/{category.id}/products',
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

    category = categories.add(Category(name='Men'))

    r = client.post(
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_401_UNAUTHORIZED
    assert payload['message'] == 'Incorrect authentication credentials.'


def test_add_product_not_active_user(client):
    category = categories.add(Category(name='Men'))

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.role = UserRole.ADMIN

    access_token = create_access_token(user.id)

    r = client.post(
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You have not active account.'


def test_add_product_not_logged_in(client):
    category = categories.add(Category(name='Men'))

    r = client.post(
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_not_admin_or_worker(client):
    category = categories.add(Category(name='Men'))

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

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.post(
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_missing_name(client):
    category = categories.add(Category(name='Men'))

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'price': 213.99,
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_missing_price(client):
    category = categories.add(Category(name='Men'))

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
        f'/api/categories/{category.id}/products',
        data=json.dumps({
            'name': 'New Super Product',
            'description': 'blah blah blah'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )
    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_delete_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    assert not product.is_deleted

    r = client.delete(f'/api/products/{product.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Product was successfully deleted.'
    assert product.is_deleted


def test_delete_already_deleted_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)
    products.delete(product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    assert product.is_deleted

    r = client.delete(f'/api/products/{product.id}',
                      headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_delete_not_existing_product(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

    r = client.delete(f'/api/products/{product.id}')
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_restore_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    products.delete(product)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    assert product.id
    assert product.is_deleted

    r = client.patch(
        f'/api/products/{product.id}/restore',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Product was successfully restored.'
    assert not product.is_deleted


def test_restore_not_existing_product(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    not_existing_product = products.get(not_existing_product_id)
    assert not_existing_product is None

    r = client.patch(
        f'/api/products/{not_existing_product_id}/restore',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_restore_not_deleted_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    assert product.id
    assert not product.is_deleted

    r = client.patch(
        f'/api/products/{product.id}/restore',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Product is not deleted.'


def test_restore_product_not_logged_in(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    products.delete(product)
    categories.add_product(category, product)

    r = client.patch(f'/api/products/{product.id}/restore')
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_restore_product_not_admin_or_worker(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    products.delete(product)
    categories.add_product(category, product)

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

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.patch(f'/api/products/{product.id}/restore',
                     headers={'Authorization': f'Bearer {access_token}'})
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_image(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    r = client.post(
        f'/api/products/{product.id}/images',
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='multipart/form-data'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_image_not_admin_or_worker(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    product_without_image = Product(name='Different product', price=2.99)
    categories.add_product(category, product_without_image)

    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    image = products.add_image(product, url='fake_url.jpg')

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True
    user.role = UserRole.ADMIN

    assert product.id

    r = client.delete(f'/api/products/{product.id}/images/{image.id}')
    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_product(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    assert product.name == 'Super Small Product'
    assert product.count == 0

    r = client.patch(
        f'/api/products/{product.id}',
        data=json.dumps({
            'name': 'Super Big Product',
            'count': 5
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Product was successfully modified.'
    assert product.name == 'Super Big Product'
    assert product.count == 5


def test_update_no_data(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    assert product.name == 'Super Small Product'

    r = client.patch(
        f'/api/products/{product.id}',
        headers={'Authorization': f'Bearer {access_token}'},
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_product_not_logged_in(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    r = client.patch(
        f'/api/products/{product.id}',
        data=json.dumps({
            'name': 'Super Big Product',
            'price': 0.99,
            'category_id': category.id
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_product_not_admin_or_worker(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.patch(
        f'/api/products/{product.id}',
        data=json.dumps({
            'name': 'Super Big Product',
            'price': 0.99,
            'category_id': category.id
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_not_existing_product(client):
    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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
    not_existing_category_id = 100

    r = client.patch(
        f'/api/products/{not_existing_product_id}',
        data=json.dumps({
            'name': 'Super Big Product',
            'price': 0.99,
            'category_id': not_existing_category_id
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_add_product_rating(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    r = client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({
            'rating': 5
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Rating was successfully added.'
    assert len(product.ratings) == 1
    assert product.ratings[0] is not None
    assert product.ratings[0].rating == 5


def test_add_product_rating_out_of_range(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    r = client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({
            'rating': 6
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Rating must be integer between 1 and 5.'


def test_add_product_rating_not_number(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    r = client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({
            'rating': 'not_a_number'
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Rating must be integer between 1 and 5.'


def test_add_product_rating_not_existing_product(client):
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

    not_existing_product_id = 99

    r = client.post(
        f'/api/products/{not_existing_product_id}/ratings',
        data=json.dumps({
            'rating': 5
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_add_product_rating_not_logged_in(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    r = client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({
            'rating': 5
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_add_product_rating_empty_json(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    r = client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({}),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_add_product_rating_second_time(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({
            'rating': 5
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    assert product.ratings[0].user == user

    r = client.post(
        f'/api/products/{product.id}/ratings',
        data=json.dumps({
            'rating': 5
        }),
        headers={'Authorization': f'Bearer {access_token}'},
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'This user already rated this product.'


def test_get_product_ratings(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user1 = users.add(User(email='user1@server.com', password='blah'))
    user2 = users.add(User(email='user2@server.com', password='blah'))
    user3 = users.add(User(email='user3@server.com', password='blah'))

    assert user1.id == 1
    assert user2.id == 2
    assert user3.id == 3

    products.add_rating(product, user1, 5)
    products.add_rating(product, user2, 4)
    products.add_rating(product, user3, 3)

    r = client.get(f'/api/products/{product.id}/ratings')

    payload = r.json

    product_ratings = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(product_ratings) == 3

    sorted_product_ratings = sorted(product_ratings, key=lambda rating: rating['user']['id'])

    assert sorted_product_ratings[0]['user']['id'] == 1
    assert sorted_product_ratings[1]['user']['id'] == 2
    assert sorted_product_ratings[2]['user']['id'] == 3

    assert sorted_product_ratings[0]['user']['email'] == 'user1@server.com'
    assert sorted_product_ratings[1]['user']['email'] == 'user2@server.com'
    assert sorted_product_ratings[2]['user']['email'] == 'user3@server.com'

    assert sorted_product_ratings[0]['product']['id'] == product.id
    assert sorted_product_ratings[1]['product']['id'] == product.id
    assert sorted_product_ratings[2]['product']['id'] == product.id

    assert sorted_product_ratings[0]['rating'] == 5
    assert sorted_product_ratings[1]['rating'] == 4
    assert sorted_product_ratings[2]['rating'] == 3


def test_get_not_existing_product_ratings(client):
    not_existing_product_id = 99

    r = client.get(f'/api/products/{not_existing_product_id}/ratings')

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_delete_product_rating(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True

    products.add_rating(product, user, 5)

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

    assert len(product.ratings) == 1

    r = client.delete(
        f'/api/products/{product.id}/ratings',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Rating was successfully deleted.'
    assert len(product.ratings) == 0


def test_delete_product_rating_on_not_existing_product(client):
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

    not_existing_product_id = 99

    r = client.delete(
        f'/api/products/{not_existing_product_id}/ratings',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_delete_not_existing_product_rating(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

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

    assert len(product.ratings) == 0

    r = client.delete(
        f'/api/products/{product.id}/ratings',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Rating not found.'


def test_delete_product_rating_not_logged_in(client):
    category = categories.add(Category(name='Men'))
    product = Product(name='Super Small Product', price=0.99)
    categories.add_product(category, product)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
    user.active = True

    products.add_rating(product, user, 5)

    r = client.delete(f'/api/products/{product.id}/ratings')

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_all_deleted_products(client):
    category = categories.add(Category(name='Men'))
    product1 = Product(name='Product One', price=13.99)
    product2 = Product(name='Product Two', price=23.99, description='blah')
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, Product(name='Product Three', price=3.99))
    categories.add_product(category, Product(name='Product Four', price=68.99))
    products.delete(product1)
    products.delete(product2)

    user = users.add(User(email='tibor@mikita.eu', password='blah'))
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

    r = client.get(
        '/api/products/deleted',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    all_deleted_products = payload

    assert r.status_code == status.HTTP_200_OK
    assert len(all_deleted_products) == 2

    sorted_products = sorted(all_deleted_products, key=lambda product_: product_['id'])

    assert sorted_products[0]['name'] == 'Product One'
    assert sorted_products[1]['name'] == 'Product Two'

    assert sorted_products[0]['price'] == 13.99
    assert sorted_products[1]['price'] == 23.99

    assert sorted_products[0]['description'] is None
    assert sorted_products[1]['description'] == 'blah'

    assert sorted_products[0]['category']['name'] == \
           sorted_products[1]['category']['name'] == \
           'Men'


def test_get_all_deleted_products_not_logged_in(client):
    r = client.get('/api/products/deleted')

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_all_deleted_products_not_admin_or_worker(client):
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

    assert user.role != UserRole.ADMIN and user.role != UserRole.WORKER

    r = client.get(
        '/api/products/deleted',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'
