from time import time

from . import r
from config import server_config
import jwt

USER_TOKEN_PREFIX = server_config.get('server', 'user_token_prefix')
SECERT = server_config.get('server', 'secret')
JWT_ALGORITHM = 'HS256'


def get_user_token(user_id, username):
    return {
        'userID': user_id,
        'username': username,
        'createTime': time(),
    }


def add_token(user_id, username, expire=2592000):
    token = jwt.encode(get_user_token(user_id, username), SECERT, algorithm=JWT_ALGORITHM).decode()
    r.set(USER_TOKEN_PREFIX + user_id, token, expire)
    return token


def get_token(user_id):
    # return None if find nothing
    return r.get(USER_TOKEN_PREFIX + user_id)


def remove_token(user_id):
    r.delete(USER_TOKEN_PREFIX + user_id)
