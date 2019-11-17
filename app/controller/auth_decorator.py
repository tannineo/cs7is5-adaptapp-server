from functools import wraps
from flask import request, current_app, g
import jwt

from config import server_config
from service import user as user_service
from constant import UserRole

SECRET = server_config.get('server', 'secret')


# get authorization header from that magical request
def login_required(roles=[UserRole.USER]):
    def real_deco(function):
        @wraps(function)
        def decorator(*args, **kwargs):
            auth = request.headers.get('Authorization')
            current_app.logger.info('authorization:' + auth)
            try:
                token_data = jwt.decode(auth, SECRET, algorithms='HS256')
                current_app.logger.info('token_data:' + str(token_data))
            except Exception:
                raise Exception('Invalid token')

            if not token_data:
                raise Exception('invalid token')
            if not token_data['userID']:
                raise Exception('invalid token')

            # search for the user
            user = user_service.find_user_by_user_id_for_token(
                token_data['userID'])

            for r in roles:
                if r.value not in user.roles:
                    raise Exception('need authorization: ' + r)

            g.user = user
            g.user_id = str(user.id)

            return function(*args, **kwargs)

        return decorator

    return real_deco
