from flask import request, g
from flask_restplus import Namespace, Resource, fields
from mongoengine.errors import ValidationError

from service.user import recommender
from service.picture import get_by_tag, upload
from .auth_decorator import login_required

picture_api = Namespace(
    'picture',
    description='Picture Controller, search, recommend, like and upload')


@picture_api.route('/search')
class PictureSearch(Resource):
    @picture_api.doc('search')
    @login_required()
    def get(self):
        search_str = request.args.get("search")
        if (search_str == ''):
            raise Exception('empty search string')

        # pictures = get_by_tag(search_str)
        # return {'msg': 'OK', 'result': {'picutres': pictures.to_json()}}

        return {
            'msg': 'OK',
            'result': {
                'prefix':
                'http://34.65.122.100:4000/img/',
                'pictures': [{
                    'id': 'aaa111',
                    'name': 'horse-00001',
                    'url': '/00001-horse.jpg'
                }, {
                    'id': 'bbb111',
                    'name': 'cat-00001',
                    'url': '/00001-cat.jpg'
                }, {
                    'id': 'ccc111',
                    'name': 'elephant-00001',
                    'url': '/00001-elephant.jpg'
                }, {
                    'id': 'ddd111',
                    'name': 'dog-00001',
                    'url': '/00001-dog.jpg'
                }, {
                    'id': 'eee111',
                    'name': 'squirrel-00001',
                    'url': '/00001-squirrel.jpg'
                }]
            }
        }


@picture_api.route('/recommend')
class PictureRecommend(Resource):
    @picture_api.doc('recommend')
    @login_required()
    def get(self):

        # user = g.user
        # picture_ids = []
        # picture_ids = recommender(g.user_id)

        # pictures
        # if (picture_ids == []):
        #     tag = user.tags[0]
        #     pictures = get_by_tag(tag)

        # else:
        #     pictures = Picture.objects(_id__in=picture_ids)

        # return {'msg': 'OK', 'result': pictures.to_json()}

        return {
            'msg': 'OK',
            'result': {
                'prefix':
                'http://34.65.122.100:4000/img/',
                'pictures': [{
                    'id': 'aaa111',
                    'name': 'horse-00001',
                    'url': '/00001-horse.jpg'
                }, {
                    'id': 'bbb111',
                    'name': 'cat-00001',
                    'url': '/00001-cat.jpg'
                }, {
                    'id': 'ccc111',
                    'name': 'elephant-00001',
                    'url': '/00001-elephant.jpg'
                }, {
                    'id': 'ddd111',
                    'name': 'dog-00001',
                    'url': '/00001-dog.jpg'
                }, {
                    'id': 'eee111',
                    'name': 'squirrel-00001',
                    'url': '/00001-squirrel.jpg'
                }]
            }
        }


like_fields = picture_api.model(
    'like', {
        'pic_id': fields.Integer(required=True, description='picture id'),
    })


@picture_api.route('/like')
class PictureLike(Resource):
    @picture_api.doc('like', body=like_fields)
    @login_required()
    def post(self):

        json = request.get_json()

        if not json['pic_id']:
            raise Exception('pic_id is required.')

        # pic_id = json['pic_id']
        # picture = Picture.objects(id=pic_id)

        # user = g.user
        # user.update(push__likes=picture)

        return {
            'msg': 'OK',
        }


upload_fields = picture_api.model(
    'upload', {
        'name':
        fields.String(required=True, description='name'),
        'img_url':
        fields.String(required=True, description='image url'),
        'tags':
        fields.List(
            cls_or_instance=fields.String, required=True, description='tags'),
    })


@picture_api.route('/upload')
class PictureUpload(Resource):
    @picture_api.doc('upload', body=upload_fields)
    @login_required()
    def post(self):
        json = request.get_json()
        """validate req data"""
        error = None

        if not json['name']:
            error = 'Name is required.'
        if not json['img_url']:
            error = 'Image url is required.'
        if not json['tags']:
            error = 'Tags field is required.'

        if error is None:
            """service logic"""
            picture = upload(name=json['name'],
                             image=json['img_url'],
                             tags=json['tags'])
            print(picture.to_json())
            return {'msg': 'OK', 'result': picture.to_json()}

        else:
            return {'msg': error}, 400
