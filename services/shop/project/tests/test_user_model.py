import datetime

import pytest

from project.models.user import User, UserRole, Country


def test_create(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.email == 'tibor@mikita.eu'
    assert user.id is None
    assert user.first_name is None


def test_create_email_invalid_type(app):
    with pytest.raises(TypeError) as e:
        User(None, 'blah')

    assert str(e.value) =='Email must be string.'


def test_create_invalid_email_format(app):
    with pytest.raises(ValueError) as e:
        User('tibor.mikita.eu', 'blah')

    assert str(e.value) =='Invalid email format.'


def test_create_password_invalid_type(app):
    with pytest.raises(TypeError) as e:
        User('tibor@mikita.eu', 555)

    assert str(e.value) =='Password must be string.'


def test_create_password_short(app):
    with pytest.raises(ValueError) as e:
        User('tibor@mikita.eu', 'abc')

    assert str(e.value) =='Password must have between 4 and 15 chars, ' \
                              'it must start with letter and can only be used letters, ' \
                              'numbers and underscore.'


def test_create_password_long(app):
    with pytest.raises(ValueError) as e:
        User('tibor@mikita.eu', 'aaaaa11111000001')

    assert str(e.value) =='Password must have between 4 and 15 chars, ' \
                              'it must start with letter and can only be used letters, ' \
                              'numbers and underscore.'


def test_create_password_starts_with_number(app):
    with pytest.raises(ValueError) as e:
        User('tibor@mikita.eu', '1aaaa')

    assert str(e.value) =='Password must have between 4 and 15 chars, ' \
                              'it must start with letter and can only be used letters, ' \
                              'numbers and underscore.'


def test_create_password_special_chars(app):
    with pytest.raises(ValueError) as e:
        User('tibor@mikita.eu', 'd%#$@')

    assert str(e.value) =='Password must have between 4 and 15 chars, ' \
                              'it must start with letter and can only be used letters, ' \
                              'numbers and underscore.'


def test_set_active(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.active is False

    user.active = True

    assert user.active is True


def test_set_active_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.active = 'True'

    assert str(e.value) =='Active flag must be boolean.'


def test_unset_active(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.active = None

    assert str(e.value) =='Active flag must be boolean.'


def test_set_phone(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.phone is None

    user.phone = '+421111222333'

    assert user.phone == '+421111222333'


def test_set_phone_invalid_prefix(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(ValueError) as e:
        user.phone = '+428111222333'

    assert 'Phone must have format' in str(e.value)


def test_set_phone_invalid_format(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(ValueError) as e:
        user.phone = '0111222333'

    assert 'Phone must have format' in str(e.value)


def test_set_phone_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.phone = 111222333

    assert str(e.value) =='Phone must be string.'


def test_set_role(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.role == UserRole.CUSTOMER

    user.role = UserRole.ADMIN

    assert user.role == UserRole.ADMIN


def test_set_role_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.role = "ADMIN"

    assert 'Role must be integer value from this set: ' in str(e.value)


def test_set_role_out_of_range(app):
    user = User('tibor@mikita.eu', 'blah')

    not_existing_user_role_value = 9

    assert not_existing_user_role_value not in [value.value for value in UserRole.__members__.values()]

    with pytest.raises(TypeError) as e:
        user.role = not_existing_user_role_value

    assert 'Role must be integer value from this set: ' in str(e.value)


def test_unset_role(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.role = None

        assert 'Role must be integer value from this set: ' in str(e.value)


def test_set_first_name(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.first_name is None

    user.first_name = 'Tibor'

    assert user.first_name == 'Tibor'


def test_unset_first_name(app):
    user = User('tibor@mikita.eu', 'blah', first_name='Tibor')

    assert user.first_name is not None

    user.first_name = None

    assert user.first_name is None


def test_set_first_name_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.first_name = 555

    assert str(e.value) =='First name must be string.'


def test_set_last_name(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.last_name is None

    user.last_name = 'Mikita'

    assert user.last_name == 'Mikita'


def test_unset_last_name(app):
    user = User('tibor@mikita.eu', 'blah', last_name='Mikita')

    assert user.last_name is not None

    user.last_name = None

    assert user.last_name is None


def test_set_last_name_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.last_name = 555

    assert str(e.value) =='Last name must be string.'


def test_set_street(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.street is None

    user.street = 'Kosicka'

    assert user.street == 'Kosicka'


def test_unset_street(app):
    user = User('tibor@mikita.eu', 'blah', street='Kosicka')

    assert user.street is not None

    user.street = None

    assert user.street is None


def test_set_street_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.street = 555

    assert str(e.value) =='Street must be string.'


def test_set_zip_code(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.zip_code is None

    user.zip_code = '06601'

    assert user.zip_code == '06601'


def test_set_zip_code_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.zip_code = 56601

    assert str(e.value) =='ZIP code must be string.'


def test_set_zip_code_invalid_format(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(ValueError) as e:
        user.zip_code = '060a1'

    assert str(e.value) =='ZIP code must contain 5 numbers.'


def test_set_zip_code_short(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(ValueError) as e:
        user.zip_code = '0666'

    assert str(e.value) =='ZIP code must contain 5 numbers.'


def test_set_zip_code_long(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(ValueError) as e:
        user.zip_code = '066666'

    assert str(e.value) =='ZIP code must contain 5 numbers.'


def test_unset_zip_code(app):
    user = User('tibor@mikita.eu', 'blah', zip_code='06601')

    assert user.zip_code is not None

    user.zip_code = None

    assert user.zip_code is None


def test_set_country(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.country is None

    user.country = Country.SK

    assert user.country == Country.SK


def test_set_country_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.country = 'SK'

    assert 'Country must be integer value from this set:' in str(e.value)


def test_set_country_out_of_range(app):
    user = User('tibor@mikita.eu', 'blah')

    not_existing_country_value = 9

    assert not_existing_country_value not in [value.value for value in Country.__members__.values()]

    with pytest.raises(TypeError) as e:
        user.country = not_existing_country_value

    assert 'Country must be integer value from this set:' in str(e.value)


def test_unset_country(app):
    user = User('tibor@mikita.eu', 'blah', country=Country.SK)

    assert user.country is not None

    user.country = None

    assert user.zip_code is None


def test_set_date_of_birth(app):
    user = User('tibor@mikita.eu', 'blah')

    assert user.date_of_birth is None

    user.date_of_birth = datetime.date(1996, 2, 20)

    assert user.date_of_birth == datetime.date(1996, 2, 20)


def test_set_date_of_birth_invalid_type(app):
    user = User('tibor@mikita.eu', 'blah')

    with pytest.raises(TypeError) as e:
        user.date_of_birth = '19.2.2018'

    assert str(e.value) =='Date of birth must be date.'


def test_unset_date_of_birth(app):
    user = User('tibor@mikita.eu', 'blah', date_of_birth=datetime.date(1996, 2, 20))

    assert user.date_of_birth is not None

    user.date_of_birth = None

    assert user.date_of_birth is None
