from flask import request
from flask_restplus import Namespace, Resource, fields

from service.user import create_user

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

        try:
            """validate req data"""
            error = None

            if not json['username']:
                error = 'Username is required.'
            elif not json['password_not_hashed']:
                error = 'Password is required.'
            elif not json['email']:
                error = 'Email is required.'

            if error is None:
                """service logic"""
            error = create_user(username=json['username'],
                                password=json['password_not_hashed'],
                                email=json['email'])
            # register service
        except Exception as e:
            return {'msg': str(e)}, 500  # specify the error code
        else:
            pass

        return {'msg': 'OK', 'result': json['username']}


login_fields = user_api.model(
    'login', {
        'username':
        fields.String(required=True, description='username'),
        'password_not_hashed':
        fields.String(required=True, description='password'),
    })


@user_api.route('/login')
class UserLogin(Resource):
    @user_api.doc('user_login', body=login_fields)
    def post(self):
        json = request.get_json()
        print(json)

        return {'msg': 'OK'}


@user_api.route('/logout')
class UserLogout(Resource):
    @user_api.doc('user_logout')
    def get():
        return {'msg': 'OK'}


@user_api.route('/config')
class UserConfig(Resource):
    @user_api.doc('user_config')
    def get():
        return {'msg': 'OK'}

    @user_api.doc('user_config_update')
    def post():
        return {'msg': 'OK'}


@user_api.route('/tags')
class UserTags(Resource):
    @user_api.doc('tags_list')
    def get():
        return {'msg': 'OK'}

    @user_api.doc('update_favorite_tags')
    def post():
        return {'msg': 'OK'}
