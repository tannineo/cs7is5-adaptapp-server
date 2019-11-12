from flask import request
from flask_restplus import Namespace, Resource, fields
from mongoengine.errors import ValidationError

pic_api = Namespace('pic',
                    description='Pic Controller, search, like, recommendation')


# TODO path variables
@pic_api.route('/like')
class PicLike(Resource):
    @pic_api.doc('like_button')
    def post(self):
        return {'msg': 'OK'}


# TODO path variables
@pic_api.route('/search')
class Search(Resource):
    @pic_api.doc('search')
    def post(self):
        return {'msg': 'OK'}


@pic_api.route('/recommend')
class PicRecommend(Resource):
    @pic_api.doc('recommendation_slide')
    def get(self):
        return {'msg': 'OK'}
