import datetime
import json

from flask.testing import FlaskClient
from flask_api import status

from project.business import users
from project.models.user import User, Country


def test_get_user(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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
        f'/api/users/{user.id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json
    user_info = payload

    assert r.status_code == status.HTTP_200_OK

    assert user_info['email'] == 'tibor@mikita.eu'
    assert user_info['first_name'] == 'Tibor'
    assert user_info['last_name'] == 'Mikita'
    assert user_info['phone'] == '+421111222333'
    assert user_info['street'] == 'Kosicka'
    assert user_info['zip_code'] == '06601'
    assert user_info['city'] == 'Humenne'
    assert user_info['country'] == Country.SK
    assert datetime.datetime.strptime(user_info['date_of_birth'], '%Y-%m-%d').date() == datetime.date(1994, 5, 25)


def test_get_not_existing_user(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    not_existing_user_id = 99
    not_existing_user = users.get(not_existing_user_id)

    assert not_existing_user is None

    r = client.get(
        f'/api/users/{not_existing_user_id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'User not found.'


def test_get_user_not_logged_in(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
    user.active = True

    r = client.get(f'/api/users/{user.id}', )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_get_other_user(client: FlaskClient):
    user = users.add(User('peter@hnat.eu', 'poaa'))
    user.active = True

    other_user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
    other_user.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'peter@hnat.eu',
            'password': 'poaa'
        }),
        content_type='application/json'
    )

    payload = r.json

    access_token = payload['access_token']

    r = client.get(
        f'/api/users/{other_user.id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'You cannot get user profile of other person.'


def test_update_user_profile(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    assert user.city == 'Humenne'
    assert user.street == 'Kosicka'
    assert user.zip_code == '06601'
    assert user.phone == '+421111222333'
    assert user.country == Country.SK

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'city': 'Medzilaborce',
            'street': 'Bratislavska',
            'zip_code': '99999',
            'phone': '+420999999999',
            'country': 0
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Profile successfully modified.'

    assert user.city == 'Medzilaborce'
    assert user.street == 'Bratislavska'
    assert user.zip_code == '99999'
    assert user.phone == '+420999999999'
    assert user.country == Country.CZ


def test_update_user_profile_remove_something(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    assert user.street == 'Kosicka'

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'street': None,
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_200_OK
    assert payload['message'] == 'Profile successfully modified.'

    assert user.street is None


def test_update_user_profile_invalid_country_code(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.CZ,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    assert user.city == 'Humenne'
    assert user.street == 'Kosicka'
    assert user.zip_code == '06601'
    assert user.phone == '+421111222333'

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'city': 'Medzilaborce',
            'street': 'Bratislavska',
            'zip_code': '99999',
            'phone': '+420999999999',
            'country': 3
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'is not a valid Country' in payload['message']


def test_update_user_profile_not_logged_in(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
    user.active = True

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'city': 'Medzilaborce',
            'street': 'Bratislavska',
            'zip_code': '99999',
            'phone': '+420999999999'
        }),
        content_type='application/json'
    )

    payload = r.json

    assert r.status_code == status.HTTP_403_FORBIDDEN
    assert payload['message'] == 'You do not have permission to perform this action.'


def test_update_not_existing_user_profile(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    not_existing_user_id = 99
    not_existing_user = users.get(not_existing_user_id)

    assert not_existing_user is None

    r = client.patch(
        f'/api/users/{not_existing_user_id}',
        data=json.dumps({
            'city': 'Medzilaborce',
            'street': 'Bratislavska',
            'zip_code': '99999',
            'phone': '+420999999999'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert payload['message'] == 'User not found.'


def test_update_other_user_profile_not_mine(client: FlaskClient):
    user1 = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
    user1.active = True

    user2 = users.add(User('peter@gnat.eu', 'dsaa'))
    user2.active = True

    r = client.post(
        '/api/auth/login',
        data=json.dumps({
            'email': 'peter@gnat.eu',
            'password': 'dsaa'
        }),
        content_type='application/json'
    )

    payload = r.json

    access_token = payload['access_token']

    r = client.patch(
        f'/api/users/{user1.id}',
        data=json.dumps({
            'city': 'Medzilaborce',
            'street': 'Bratislavska',
            'zip_code': '99999',
            'phone': '+420999999999'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'You cannot edit profile of other person.'


def test_update_user_profile_empty(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_user_profile_no_data(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    r = client.patch(
        f'/api/users/{user.id}',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_user_profile_not_existing_attribute(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    assert user.city == 'Humenne'
    assert user.street == 'Kosicka'
    assert user.zip_code == '06601'
    assert user.phone == '+421111222333'

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'number': '42'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Invalid payload.'


def test_update_user_profile_date_invalid_type(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'date_of_birth': 5
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert payload['message'] == 'Date of birth must be date.'


def test_update_user_profile_invalid_phone_format(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'phone': '0999999999'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Phone must have format' in payload['message']


def test_update_user_profile_transaction(client: FlaskClient):
    user = users.add(
        User(
            email='tibor@mikita.eu',
            password='blah',
            first_name='Tibor',
            last_name='Mikita',
            phone='+421111222333',
            street='Kosicka',
            zip_code='06601',
            city='Humenne',
            country=Country.SK,
            date_of_birth=datetime.date(1994, 5, 25)
        )
    )
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

    assert user.first_name == 'Tibor'

    r = client.patch(
        f'/api/users/{user.id}',
        data=json.dumps({
            'city': 'Presov',
            'phone': '0999999999'
        }),
        content_type='application/json',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    payload = r.json

    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert 'Phone must have format' in payload['message']

    user_after_update = users.get(user.id)

    assert user_after_update.city == 'Humenne'
