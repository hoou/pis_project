from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError
from flask_restplus import Api
from jwt.exceptions import DecodeError, ExpiredSignatureError

from project.api.errors import PermissionDenied, ParseError, ExpiredAccessToken

api = Api()


@api.errorhandler(NoAuthorizationError)
def handle_no_authorization_errror(error):
    return {'message': PermissionDenied.description}, PermissionDenied.code


@api.errorhandler(InvalidHeaderError)
def handle_invalid_header_errror(error):
    return {'message': ParseError.description}, ParseError.code


@api.errorhandler(DecodeError)
def handle_decode_error(error):
    return {'message': ParseError.description}, ParseError.code


@api.errorhandler(ExpiredSignatureError)
def handle_expired_signature_error(error):
    return {'message': ExpiredAccessToken.description}, ExpiredAccessToken.code
