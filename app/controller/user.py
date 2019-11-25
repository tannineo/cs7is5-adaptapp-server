from flask import request, g, current_app
from flask_restplus import Namespace, Resource, fields

import service.user as user_service
from service.tag import get_initial_tag_list
from .auth_decorator import login_required

user_api = Namespace(
    'user',
    description='User Controller, register, login, logout & account settings')

# swagger header doc
user_auth_header_parser = user_api.parser()
user_auth_header_parser.add_argument(
    'Authorization',
    location='headers',
    help='the authorization where the token is')

register_fields = user_api.model(
    'register', {
        'username': fields.String(required=True, description='username'),
        'password_not_hashed': fields.String(required=True,
                                             description='password'),
        'email': fields.String(required=True, description='email'),
    })


@user_api.route('/register')
class UserRegister(Resource):
    @user_api.doc('user_register', body=register_fields)
    def post(self):
        json = request.get_json()

        if not json['username']:
            raise Exception('Username is required.')
        elif not json['password_not_hashed']:
            raise Exception('Password is required.')
        elif not json['email']:
            raise Exception('Email is required.')

        user_service.create_user(
            username=json['username'],
            password_not_hashed=json['password_not_hashed'],
            email=json['email'])

        return {'msg': 'OK', 'result': json['username']}


login_fields = user_api.model(
    'login', {
        'username':
        fields.String(required=True, description='username'),
        'password_not_hashed':
        fields.String(required=True, description='password_not_hashed'),
    })


@user_api.route('/login')
class UserLogin(Resource):
    @user_api.doc('user_login', body=login_fields)
    def post(self):
        json = request.get_json()

        if not json['username']:
            raise Exception('Username is required.')
        elif not json['password_not_hashed']:
            raise Exception('Password is required.')

        # service logic
        token, tags, force_pic_config = user_service.user_login(
            username=json['username'],
            password_not_hashed=json['password_not_hashed'])

        network_status = user_service.user_network_status(g.user_id)

        return {
            'msg': 'OK',
            'result': {
                'token': token,
                'tags': tags,
                'force_pic_config': force_pic_config,
                'network_status': network_status
            }
        }


@user_api.route('/logout')
@user_api.header('Authorization', 'the authorization where the token is')
@user_api.expect(user_auth_header_parser)
class UserLogout(Resource):
    @user_api.doc('user_logout')
    @login_required()
    def get(self):
        user_service.user_logout(g.user_id)
        return {'msg': 'OK'}


user_setting_fields = user_api.model(
    'user_setting', {
        'force_pic_config':
        fields.Boolean(required=True,
                       description='true / false to show high resolution'),
        'network_status':
        fields.String(required=True, description='email'),
    })


@user_api.route('/config')
@user_api.header('Authorization', 'the authorization where the token is')
@user_api.expect(user_auth_header_parser)
class UserConfig(Resource):
    @user_api.doc('user_config')
    @login_required()
    def get(self):

        force_pic_config = g.user.force_pic_config
        network_status = user_service.user_network_status(g.user_id)

        return {
            'msg': 'OK',
            'result': {
                'force_pic_config': force_pic_config,
                'network_status': network_status
            }
        }

    @user_api.doc('user_config_update', body=user_setting_fields)
    @login_required()
    def post(self):
        json = request.get_json()

        if not json['force_pic_config']:
            raise Exception('force_pic_config is required.')
        elif not json['network_status']:
            raise Exception('network_status is required.')

        network_status = json['network_status']
        force_pic_config = json['force_pic_config']

        user_service.user_update_network_status_settings(
            g.user, network_status, force_pic_config)

        return {
            'msg': 'OK',
            'result': {
                'network_status': network_status,
                'force_pic_config': force_pic_config
            }
        }


update_user_tags = user_api.model('update_user_tags', {
    'tags':
    fields.List(fields.String(), required=True, description='username'),
})


@user_api.route('/tags')
@user_api.header('Authorization', 'the authorization where the token is')
@user_api.expect(user_auth_header_parser)
class UserTags(Resource):
    @user_api.doc('tags_list')
    @login_required()
    def get(self):
        # get suggested tags
        tags = get_initial_tag_list()
        return {'msg': 'OK', 'result': {'tags': tags}}

    @user_api.doc('update_favorite_tags', body=update_user_tags)
    @login_required()
    def post(self):
        json = request.get_json()

        if not json['tags']:
            raise Exception('Username is required.')

        # service logic
        user_service.update_user_tags(g.user, json['tags'])

        return {'msg': 'OK', 'result': {'tags': json['tags']}}
