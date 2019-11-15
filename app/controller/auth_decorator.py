from functools import wraps
from flask import request, current_app, g
import jwt

from config import server_config
from service import user as user_service

SECRET = server_config.get('server', 'secret')


# get authorization header from that magical request
def login_required(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        auth = request.headers.get('Authorization')
        current_app.logger.info('authorization:' + auth)
        try:
            token_data = jwt.decode(auth, SECRET, algorithms='HS256')
            current_app.logger.info('token_data:' + str(token_data))
        except Exception:
            raise RuntimeError('Invalid token')

        if token_data is None:
            raise RuntimeError('invalid token')
        if token_data['userID'] is None:
            raise RuntimeError('invalid token')

        # search for the user
        user = user_service.find_user_by_user_id_for_token(
            token_data['userID'])
        g.user = user
        g.user_id = str(user.id)

        return function(*args, **kwargs)

    return decorator
