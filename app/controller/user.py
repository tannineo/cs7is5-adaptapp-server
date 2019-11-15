from flask import request, g, current_app
from flask_restplus import Namespace, Resource, fields

import service.user as user_service
from service.tag import get_initial_tag_list
from .auth_decorator import login_required

user_api = Namespace(
    'user',
    description='User Controller, register, login, logout & account settings')

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
            raise RuntimeError('Username is required.')
        elif not json['password_not_hashed']:
            raise RuntimeError('Password is required.')
        elif not json['email']:
            raise RuntimeError('Email is required.')

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
            raise RuntimeError('Username is required.')
        elif not json['password_not_hashed']:
            raise RuntimeError('Password is required.')

        # service logic
        token, tags = user_service.user_login(
            username=json['username'],
            password_not_hashed=json['password_not_hashed'])

        return {'msg': 'OK', 'result': {'token': token, 'tags': tags}}


user_logout_parser = user_api.parser()
user_logout_parser.add_argument('Authorization',
                                location='headers',
                                help='the authorization where the token is')


@user_api.route('/logout')
@user_api.header('Authorization', 'the authorization where the token is')
@user_api.expect(user_logout_parser)
class UserLogout(Resource):
    @user_api.doc('user_logout')
    @login_required()
    def get(self):
        user_service.user_logout(g.user_id)
        return {'msg': 'OK'}


@user_api.route('/config')
@user_api.header('Authorization', 'the authorization where the token is')
@user_api.expect(user_logout_parser)
class UserConfig(Resource):
    @user_api.doc('user_config')
    @login_required()
    def get(self):
        return {'msg': 'OK'}

    @user_api.doc('user_config_update')
    @login_required()
    def post(self):
        return {'msg': 'OK'}


update_user_tags = user_api.model('update_user_tags', {
    'tags':
    fields.List(fields.String(), required=True, description='username'),
})


@user_api.route('/tags')
@user_api.header('Authorization', 'the authorization where the token is')
@user_api.expect(user_logout_parser)
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
            raise RuntimeError('Username is required.')

        # service logic
        user_service.update_user_tags(g.user, json['tags'])

        return {'msg': 'OK', 'result': {'tags': json['tags']}}
