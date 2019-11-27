from flask import current_app, g

from common import md5
from constant import UserNetworkSetting, isInEnum
from model.user import User
from model.tag import Tag
from config import server_config
from cache.token import add_token, remove_token, get_token
import cache.network as cache_network

SECRET = server_config.get('server', 'secret')


def find_user_by_user_id_for_token(user_id):
    # validate cached token
    token = get_token(user_id)
    if not token:
        raise Exception('invalid token')

    # search for user
    users = User.objects(id=user_id)
    if len(users) <= 0:
        raise Exception('no such user')

    current_app.logger.info('found user with id:' + user_id)

    return users[0]


def get_hashed_password(password_not_hashed):
    return md5(password_not_hashed, SECRET)


def create_user(username, password_not_hashed, email):
    current_app.logger.info('create user with username:' + username +
                            ' email:' + email)
    # create a user, but check if user exists first
    if User.objects(username=username).count() > 0:
        raise Exception('username already exists')
    if User.objects(email=email).count() > 0:
        raise Exception('email already exists')

    # md5 hash the string
    hashed_password = get_hashed_password(password_not_hashed)

    # save the user
    user = User()
    user.username = username
    user.password = hashed_password
    user.email = email
    user.tags = []
    user.likes = []
    user.save()

    current_app.logger.info('create user with id:' + str(user.id))

    return None


def user_login(username, password_not_hashed):
    # user login, find the user first
    login_users = User.objects(username=username)

    if len(login_users) != 1:
        raise Exception('user not exists')

    login_user = login_users[0]

    if login_user.password != get_hashed_password(password_not_hashed):
        raise Exception('password is not correct')

    login_user_id = str(login_user.id)

    # then delete the existing token
    remove_token(login_user_id)

    # generate the new token
    token = add_token(login_user_id, login_user.username)
    tags = login_user.tags
    force_pic_config = login_user.force_pic_config

    g.user = login_user
    g.user_id = str(login_user.id)

    return token, tags, force_pic_config


def user_network_status(user_id):
    # network_status
    network_status = cache_network.get_network_settings(user_id)
    if not network_status:
        network_status = UserNetworkSetting.UNKNOWN.value
    else:
        network_status = network_status.decode('utf-8')
    return network_status


def user_logout(user_id):
    # simply remove user token
    current_app.logger.info('user logout: ' + user_id)
    remove_token(user_id)


def update_user_tags(user, tags=[]):
    for t in tags:
        current_app.logger.info('searching tag: ' + t)
        if Tag.objects(name=t).count() <= 0:
            raise Exception('tag: ' + t + ' is not in the system')
    user.tags = tags
    user.save()

    current_app.logger.info('user: ' + str(user.id) + ' saved tags')


def user_update_network_status_settings(user, network_status,
                                        force_pic_config):

    if not isInEnum(network_status, UserNetworkSetting):
        raise Exception('invalide network_status')

    # save force_pic_config into user model
    user.force_pic_config = force_pic_config
    user.save()

    # update network_status in cache
    cache_network.add_network_settings(str(user.id), network_status)


# toggle on off
def user_like_a_pic(user, pic_id):
    if pic_id in user.likes:
        user.likes.remove(pic_id)
        user.save()
        return -1
    else:
        user.likes.append(pic_id)
        user.save()
        return 1


def recommender(target_user_id):
    users = User.objects
    users_list = []
    for u in users:
        pics_list = []
        for pic in u.likes:
            pics_list.append(pic._id)
        users_list.append({"userid": u._id, "pics": pics_list})

    #resulting list looks like :
    # [
    #     {
    #         "userid" : 1,
    #         "pics" : [1,2,3]
    #     },
    #     {
    #         "userid" : 2,
    #         "pics" : [3,4]
    #     },
    # ]

    # TODO: Call recommender system
    recommended_picture_ids_list = []
    # recommended_picture_ids_list = RECOMMENDER(users_list, target_user_id)
    return recommended_picture_ids_list
