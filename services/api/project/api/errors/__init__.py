from flask_api import status
from werkzeug.exceptions import HTTPException


class BadRequest(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    description = (
        'Bad request.'
    )


class InvalidPayload(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    description = (
        'Invalid payload.'
    )


class ParseError(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    description = (
        'Malformed request.'
    )


class WrongTypeOfTokenError(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    description = (
        'Wrong type of token given.'
    )


class ProductRatingError(HTTPException):
    code = status.HTTP_400_BAD_REQUEST
    description = (
        'Rating must be integer between 1 and 5.'
    )


class AuthenticationFailed(HTTPException):
    code = status.HTTP_401_UNAUTHORIZED
    description = (
        'Incorrect authentication credentials.'
    )


class ExpiredToken(HTTPException):
    code = status.HTTP_401_UNAUTHORIZED
    description = (
        'Expired token.'
    )


class InvalidAccessToken(HTTPException):
    code = status.HTTP_401_UNAUTHORIZED
    description = (
        'Invalid access token.'
    )


class PermissionDenied(HTTPException):
    code = status.HTTP_403_FORBIDDEN
    description = (
        'You do not have permission to perform this action.'
    )


class NotFound(HTTPException):
    code = status.HTTP_404_NOT_FOUND
    description = (
        'This resource does not exist.'
    )
