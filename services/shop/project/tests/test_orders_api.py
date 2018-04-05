import json
from typing import List

from flask_api import status

from project.business import users, categories, orders
from project.models.delivery_address import DeliveryAddress
from project.models.order import OrderStatus, Order
from project.models.order_item import OrderItem
from project.models.product import Product
from project.models.user import UserRole


def test_create_order_logged_in(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Order was successfully created.'

    last_user_order = orders.get_last_by_user(user)

    assert last_user_order.delivery_address.first_name == 'Tibor'
    assert last_user_order.delivery_address.last_name == 'Mikita'
    assert last_user_order.delivery_address.phone == '+421000111222'
    assert last_user_order.delivery_address.street == 'Kolejni'
    assert last_user_order.delivery_address.zip_code == '00000'
    assert last_user_order.delivery_address.city == 'Brno'
    assert last_user_order.delivery_address.country == 'CZ'

    assert len(last_user_order.items) == 3

    sorted_items: List[OrderItem] = sorted(last_user_order.items, key=lambda item: item.id)

    assert sorted_items[0].count == 1
    assert sorted_items[1].count == 1
    assert sorted_items[2].count == 2

    assert sorted_items[0].order_id == sorted_items[1].order_id == sorted_items[2].order_id == last_user_order.id

    assert sorted_items[0].price == product1.price
    assert sorted_items[1].price == product2.price
    assert sorted_items[2].price == product3.price

    assert sorted_items[0].product.id == product1.id
    assert sorted_items[1].product.id == product2.id
    assert sorted_items[2].product.id == product3.id

    assert last_user_order.status == OrderStatus.PENDING

    assert last_user_order.total == 1 * product1.price + 1 * product2.price + 2 * product3.price

    assert last_user_order.updated == last_user_order.created

    assert last_user_order.user_id == user.id


def test_create_order_logged_out(client):
    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    r = client.post(
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_201_CREATED
    assert payload['message'] == 'Order was successfully created.'

    last_order = orders.get_last_order()

    assert last_order.delivery_address.first_name == 'Tibor'
    assert last_order.delivery_address.last_name == 'Mikita'
    assert last_order.delivery_address.phone == '+421000111222'
    assert last_order.delivery_address.street == 'Kolejni'
    assert last_order.delivery_address.zip_code == '00000'
    assert last_order.delivery_address.city == 'Brno'
    assert last_order.delivery_address.country == 'CZ'

    assert len(last_order.items) == 3

    sorted_items: List[OrderItem] = sorted(last_order.items, key=lambda item: item.id)

    assert sorted_items[0].count == 1
    assert sorted_items[1].count == 1
    assert sorted_items[2].count == 2

    assert sorted_items[0].order_id == sorted_items[1].order_id == sorted_items[2].order_id == last_order.id

    assert sorted_items[0].price == product1.price
    assert sorted_items[1].price == product2.price
    assert sorted_items[2].price == product3.price

    assert sorted_items[0].product.id == product1.id
    assert sorted_items[1].product.id == product2.id
    assert sorted_items[2].product.id == product3.id

    assert last_order.status == OrderStatus.PENDING

    assert last_order.total == 1 * product1.price + 1 * product2.price + 2 * product3.price

    assert last_order.updated == last_order.created

    assert last_order.user_id is None


def test_create_order_not_existing_products(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': not_existing_product_id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Product not found.'


def test_create_order_zero_count(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 0
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Item count must be positive int.'


def test_create_order_negative_count(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': -1
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Item count must be positive int.'


def test_create_order_count_not_int(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 'sd'
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Item count must be positive int.'


def test_create_order_no_items(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_create_order_empty_items(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Order without items.'


def test_create_order_item_missing_product_id(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'count': 1
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_create_order_item_missing_count(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_create_order_no_delivery_address(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ]
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_create_order_delivery_address_missing_required_field(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': product2.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_create_order_same_product_different_items(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

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
        '/api/orders/',
        data=json.dumps({
            'items': [
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': product1.id,
                    'count': 1
                },
                {
                    'product_id': product3.id,
                    'count': 2
                }
            ],
            'delivery_address': {
                'first_name': 'Tibor',
                'last_name': 'Mikita',
                'phone': '+421000111222',
                'street': 'Kolejni',
                'zip_code': '00000',
                'city': 'Brno',
                'country': 'CZ'
            }
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_order_status(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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

    assert order.status == OrderStatus.PENDING

    r = client.patch(
        f'/api/orders/{order.id}',
        data=json.dumps({
            'status': OrderStatus.AWAITING_PAYMENT
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Order was successfully modified.'

    assert order.status == OrderStatus.AWAITING_PAYMENT


def test_update_order_status_not_logged_in(client):
    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

    r = client.patch(
        f'/api/orders/{order.id}',
        data=json.dumps({
            'status': OrderStatus.AWAITING_PAYMENT
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_order_status_not_admin_or_worker(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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
        f'/api/orders/{order.id}',
        data=json.dumps({
            'status': OrderStatus.AWAITING_PAYMENT
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_status_of_not_existing_order(client):
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

    not_existing_order_id = 99

    r = client.patch(
        f'/api/orders/{not_existing_order_id}',
        data=json.dumps({
            'status': OrderStatus.AWAITING_PAYMENT
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Order not found.'


def test_update_order_status_empty_json(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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

    assert order.status == OrderStatus.PENDING

    r = client.patch(
        f'/api/orders/{order.id}',
        data=json.dumps({}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_order_status_missing_status(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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

    assert order.status == OrderStatus.PENDING

    r = client.patch(
        f'/api/orders/{order.id}',
        data=json.dumps({
            'state': OrderStatus.AWAITING_PAYMENT
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_order_status_invalid_status(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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

    assert order.status == OrderStatus.PENDING

    invalid_order_status = 99

    r = client.patch(
        f'/api/orders/{order.id}',
        data=json.dumps({
            'status': invalid_order_status
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_cancel_order(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address, user.id)

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

    assert order.status != OrderStatus.CANCELLED

    r = client.patch(
        f'/api/orders/{order.id}/cancel',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Order was successfully cancelled.'

    assert order.status == OrderStatus.CANCELLED


def test_cancel_order_not_logged_in(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address, user.id)

    r = client.patch(f'/api/orders/{order.id}/cancel')

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_cancel_already_cancelled_order(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address, user.id)
    order.status = OrderStatus.CANCELLED

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

    assert order.status == OrderStatus.CANCELLED

    r = client.patch(
        f'/api/orders/{order.id}/cancel',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Order is already cancelled.'


def test_cancel_not_existing_order(client):
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

    not_existing_order_id = 99
    not_existing_order = orders.get(not_existing_order_id)

    assert not_existing_order is None

    r = client.patch(
        f'/api/orders/{not_existing_order_id}/cancel',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Order not found.'


def test_cancel_not_mine_order(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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

    assert order.user_id != user.id

    r = client.patch(
        f'/api/orders/{order.id}/cancel',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'You cannot cancel other\'s order.'


def test_get_all_orders(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True
    user.role = UserRole.ADMIN

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order1_item1 = OrderItem(1, product1.price, product1.id)
    order1_item2 = OrderItem(1, product2.price, product2.id)
    order1_item3 = OrderItem(2, product3.price, product3.id)

    order2_item1 = OrderItem(1, product1.price, product1.id)
    order2_item2 = OrderItem(3, product3.price, product3.id)

    order3_item1 = OrderItem(5, product3.price, product3.id)

    delivery_address1 = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')
    delivery_address2 = DeliveryAddress('Peter', 'Hnat', '+421999999999', 'Ecerova', '11111', 'Bratislava', 'SK')
    delivery_address3 = DeliveryAddress('Samuel', 'Jaklovsky', '+421555555555', 'Skacelova', '22222', 'Radvan', 'SK')

    order1 = orders.add([order1_item1, order1_item2, order1_item3], delivery_address1)
    order2 = orders.add([order2_item1, order2_item2], delivery_address2)
    order3 = orders.add([order3_item1], delivery_address3)

    order2.status = OrderStatus.AWAITING_PAYMENT
    order3.status = OrderStatus.COMPLETED

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
        f'/api/orders/',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    all_orders = payload

    sorted_orders = sorted(all_orders, key=lambda order: order['id'])

    assert r.status_code == status.HTTP_200_OK
    assert len(sorted_orders) == 3
    assert sorted_orders[0]['status'] == OrderStatus.PENDING
    assert sorted_orders[1]['status'] == OrderStatus.AWAITING_PAYMENT
    assert sorted_orders[2]['status'] == OrderStatus.COMPLETED
    assert sorted_orders[0]['status_name'] == 'pending'
    assert sorted_orders[1]['status_name'] == 'awaiting payment'
    assert sorted_orders[2]['status_name'] == 'completed'

    assert sorted_orders[0]['user']['id'] == sorted_orders[1]['user']['id'] == sorted_orders[2]['user']['id'] is None

    assert sorted_orders[0]['delivery_address']['first_name'] == 'Tibor'
    assert sorted_orders[1]['delivery_address']['first_name'] == 'Peter'
    assert sorted_orders[2]['delivery_address']['first_name'] == 'Samuel'

    assert sorted_orders[0]['total'] == round(1 * 19.99 + 1 * 29.99 + 2 * 39.99, 2)
    assert sorted_orders[1]['total'] == round(1 * 19.99 + 3 * 39.99, 2)
    assert sorted_orders[2]['total'] == round(5 * 39.99, 2)

    order1_items = sorted_orders[0]['items']
    order2_items = sorted_orders[1]['items']
    order3_items = sorted_orders[2]['items']
    sorted_order1_items = sorted(order1_items, key=lambda item: item['id'])
    sorted_order2_items = sorted(order2_items, key=lambda item: item['id'])
    sorted_order3_items = sorted(order3_items, key=lambda item: item['id'])

    assert len(sorted_order1_items) == 3
    assert len(sorted_order2_items) == 2
    assert len(sorted_order3_items) == 1

    assert sorted_order1_items[0]['price'] == 19.99
    assert sorted_order1_items[1]['price'] == 29.99
    assert sorted_order1_items[2]['price'] == 39.99

    assert sorted_order2_items[0]['price'] == 19.99
    assert sorted_order2_items[1]['price'] == 39.99

    assert sorted_order3_items[0]['price'] == 39.99

    assert sorted_order1_items[0]['product']['name'] == 'Product One'
    assert sorted_order1_items[1]['product']['name'] == 'Product Two'
    assert sorted_order1_items[2]['product']['name'] == 'Product Three'

    assert sorted_order2_items[0]['product']['name'] == 'Product One'
    assert sorted_order2_items[1]['product']['name'] == 'Product Three'

    assert sorted_order3_items[0]['product']['name'] == 'Product Three'


def test_get_all_orders_not_logged_in(client):
    r = client.get(f'/api/orders/')

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_all_orders_not_admin_or_worker(client):
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

    r = client.get(
        f'/api/orders/',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_order(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address, user.id)

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
        f'/api/orders/{order.id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    order = payload

    assert r.status_code == status.HTTP_200_OK

    assert order['status'] == OrderStatus.PENDING
    assert order['status_name'] == 'pending'

    assert order['user']['id'] == user.id

    assert order['delivery_address']['first_name'] == 'Tibor'

    assert order['total'] == round(1 * 19.99 + 1 * 29.99 + 2 * 39.99, 2)

    order_items = order['items']
    sorted_order_items = sorted(order_items, key=lambda item: item['id'])

    assert len(sorted_order_items) == 3

    assert sorted_order_items[0]['price'] == 19.99
    assert sorted_order_items[1]['price'] == 29.99
    assert sorted_order_items[2]['price'] == 39.99

    assert sorted_order_items[0]['product']['name'] == 'Product One'
    assert sorted_order_items[1]['product']['name'] == 'Product Two'
    assert sorted_order_items[2]['product']['name'] == 'Product Three'


def test_get_not_mine_order(client):
    user = users.add(email='tibor@mikita.eu', password='blah')
    user.active = True

    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

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
        f'/api/orders/{order.id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Order is not your\'s.'


def test_get_order_not_logged_in(client):
    category = categories.add(name='Men')
    product1 = Product(name='Product One', price=19.99)
    product2 = Product(name='Product Two', price=29.99)
    product3 = Product(name='Product Three', price=39.99)
    categories.add_product(category, product1)
    categories.add_product(category, product2)
    categories.add_product(category, product3)

    order_item1 = OrderItem(1, product1.price, product1.id)
    order_item2 = OrderItem(1, product2.price, product2.id)
    order_item3 = OrderItem(2, product3.price, product3.id)

    delivery_address = DeliveryAddress('Tibor', 'Mikita', '+421000111222', 'Kolejni', '00000', 'Brno', 'CZ')

    order = orders.add([order_item1, order_item2, order_item3], delivery_address)

    r = client.get(f'/api/orders/{order.id}')

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_not_existing_order(client):
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

    not_existing_order_id = 99
    not_existing_order = orders.get(not_existing_order_id)

    assert not_existing_order is None

    r = client.get(
        f'/api/orders/{not_existing_order_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'Order not found.'
