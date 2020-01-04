import os
import json
from functools import wraps
from flask import request, current_app
from jose import jwt
from jose.exceptions import JWTError, ExpiredSignatureError, JWTClaimsError, JWKError

from app.api_response import ApiResponse
from app.errors import ApiException

def authorize(func):
    @wraps(func)
    def authorize_handler(*args, **kwargs):
        public_key = current_app.config['PUBLIC_KEY']
        audience = current_app.config['AUDIENCE']
        token = request.headers.get('Token')
        if not public_key:
            raise ApiException(f'Public key is undefined', code='NotAuthorized')
        if not audience:
            raise ApiException(f'Audience is undefined', code='NotAuthorized')
        if not token:
            raise ApiException(f'Authorization not found', code='NotAuthorized')
        try:
            jwt.decode(token, public_key, algorithms=['RS256'], audience=audience)
        except JWTClaimsError as error:
            raise ApiException(error)
        except ExpiredSignatureError as error:
            raise ApiException(error)
        except JWTError as error:
            raise ApiException(error)
        except JWKError as error:
            raise ApiException(error)
        return func(*args, **kwargs)
    return authorize_handler