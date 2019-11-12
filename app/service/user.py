from common import md5

from model.user import User
from config import server_config
from server_error import ServerError, ServerErrorCodes

hash_secret = server_config.get('server', 'secret')


def create_user(username, password, email):
    # create a user, but check if user exists first
    if User.objects(username=username).count() > 0:
        raise ServerError(ServerErrorCodes.ERR_INPUT_ERROR,
                          message='username already exists')

    # md5 hash the string
    hashed_password = md5(password, hash_secret)

    print(hashed_password)

    # save the user
    user = User()
    user.username = username
    user.password = hashed_password
    user.email = email
    user.save()

    return None
