from flask import current_app

from common import md5
from model.user import User
from config import server_config
from cache.token import add_token, remove_token, get_token

SECRET = server_config.get('server', 'secret')


def find_user_by_user_id_for_token(user_id):
    # validate cached token
    token = get_token(user_id)
    if token is None:
        raise RuntimeError('invalid token')

    # search for user
    users = User.objects(id=user_id)
    if len(users) <= 0:
        raise RuntimeError('no such user')

    current_app.logger.info('found user with id:' + user_id)

    return users[0]


def get_hashed_password(password_not_hashed):
    return md5(password_not_hashed, SECRET)


def create_user(username, password_not_hashed, email):
    # create a user, but check if user exists first
    if User.objects(username=username).count() > 0:
        raise RuntimeError('username already exists')

    # md5 hash the string
    hashed_password = get_hashed_password(password_not_hashed)

    # save the user
    user = User()
    user.username = username
    user.password = hashed_password
    user.email = email
    user.save()

    return None


def user_login(username, password_not_hashed):
    # user login, find the user first
    login_users = User.objects(username=username)

    if len(login_users) != 1:
        raise RuntimeError('user not exists')

    login_user = login_users[0]

    if login_user.password != get_hashed_password(password_not_hashed):
        raise RuntimeError('password is not correct')

    login_user_id = str(login_user.id)

    # then delete the existing token
    remove_token(login_user_id)

    # generate the new token
    token = add_token(login_user_id, login_user.username)

    return token


def user_logout(user_id):
    # simply remove user token
    current_app.logger.info('user logout: ' + user_id)
    remove_token(user_id)
