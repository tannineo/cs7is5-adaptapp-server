from common import md5

from model.user import User
from config import server_config

hash_secret = server_config.get('server', 'secret')


def create_user(username, password, email):
    # create a user, but check if user exists first
    if User.objects(username=username).count() > 0:
        raise RuntimeError('username already exists')

    # md5 hash the string
    hashed_password = md5(password, hash_secret)

    # save the user
    user = User()
    user.username = username
    user.password = hashed_password
    user.email = email
    user.save()

    return None
