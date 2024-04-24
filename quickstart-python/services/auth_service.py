import jwt
import requests

from consts import SecretKeys
from errors import GenericUnauthorizedError
from services import get_secret


def create_jwt_token(payload: dict):
    """
    Create a JWT token with the given payload.
    """
    return jwt.encode(payload, get_secret(SecretKeys.MONDAY_SIGNING_SECRET), algorithm='HS256')


def decode_monday_jwt(token: str):
    """
    Validate a JWT token.
    """
    try:
        return jwt.decode(token, get_secret(SecretKeys.MONDAY_SIGNING_SECRET), options={"verify_aud": False},
                          algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise GenericUnauthorizedError('Token has expired')
    except jwt.InvalidSignatureError:
        raise GenericUnauthorizedError('Invalid signature, token validation failed')
    except jwt.InvalidTokenError:
        raise GenericUnauthorizedError('Invalid token')


def get_monday_token(code):
    """
    Function that exchanges a code for a monday.com token.
    """
    response = requests.post(get_secret(SecretKeys.MONDAY_OAUTH_TOKEN_PATH),
                             data={'code': code,
                                   'client_id': get_secret(SecretKeys.MONDAY_OAUTH_CLIENT_ID),
                                   'client_secret': get_secret(SecretKeys.MONDAY_OAUTH_CLIENT_SECRET)})
    response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
    return response.json()
