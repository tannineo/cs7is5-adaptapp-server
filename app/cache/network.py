from time import time
import jwt

from . import r
from config import server_config
from constant import UserNetworkSetting

USER_NETWORK_PREFIX = server_config.get('server', 'user_network_prefix')
SECERT = server_config.get('server', 'secret')
JWT_ALGORITHM = 'HS256'


def add_network_settings(user_id, network_setting: UserNetworkSetting, expire=2592000):
    r.set(USER_NETWORK_PREFIX + user_id, network_setting, expire)


def get_network_settings(user_id):
    # return None if find nothing
    return r.get(USER_NETWORK_PREFIX + user_id)


def remove_network_settings(user_id):
    r.delete(USER_NETWORK_PREFIX + user_id)
