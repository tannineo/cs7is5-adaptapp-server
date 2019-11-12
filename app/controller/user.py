from flask import request
from flask_restplus import Namespace, Resource, fields
from mongoengine.errors import ValidationError

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
        except AssertionError as error:
            # special error management on errors from mongoengine
            return {'msg': error}, 500  # specify the error code
        except RuntimeError as error:
            return {'msg': error}, 500
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
