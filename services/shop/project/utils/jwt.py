import datetime

import jwt
from flask import current_app


def encode_auth_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
            seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
        ),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }

    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    )


def decode_auth_token(token):
    payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
    return payload['sub']
