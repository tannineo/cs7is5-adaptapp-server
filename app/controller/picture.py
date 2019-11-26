from flask import request, g, current_app
from flask_restplus import Namespace, Resource, fields
from mongoengine.errors import ValidationError

from service.user import recommender, user_like_a_pic
from service.picture import get_by_tag, upload, randomly_get_pics, once_load_all, change_likes_of_pic
from .auth_decorator import login_required

picture_api = Namespace(
    'picture',
    description='Picture Controller, search, recommend, like and upload')

user_auth_header_parser = picture_api.parser()
user_auth_header_parser.add_argument(
    'Authorization',
    location='headers',
    help='the authorization where the token is')


@picture_api.route('/search')
@picture_api.header('Authorization', 'the authorization where the token is')
@picture_api.expect(user_auth_header_parser)
class PictureSearch(Resource):
    @picture_api.doc(
        'search',
        params={'search': 'An search keyword, empty to get system suggestion'})
    @login_required()
    def get(self):
        search_str = request.args.get("search")

        if search_str is None:
            current_app.logger.info('find pictures with NO search keyword')
            pictures = randomly_get_pics()
        else:
            current_app.logger.info('find pictures with search keyword:' +
                                    search_str)
            pictures = get_by_tag(search_str)

        pictures_result = []
        for pic in pictures:
            # check if liked by the user
            pic_id = str(pic.id)
            pictures_result.append({
                'id': pic_id,
                'name': pic.name,
                'url': pic.img_url,
                'isLike': pic_id in g.user.likes,
                'likes': pic.likes,
            })

        return {
            'msg': 'OK',
            'result': {
                'prefix': 'http://34.65.122.100:4000/img/',
                'pictures': pictures_result,
            }
        }


@picture_api.route('/recommend')
@picture_api.header('Authorization', 'the authorization where the token is')
@picture_api.expect(user_auth_header_parser)
class PictureRecommend(Resource):
    @picture_api.doc('recommend')
    @login_required()
    def get(self):

        # TODO: change it into recommend
        pictures = randomly_get_pics(5)

        pictures_result = []
        for pic in pictures:
            # check if liked by the user
            pic_id = str(pic.id)
            pictures_result.append({
                'id': pic_id,
                'name': pic.name,
                'url': pic.img_url,
                'isLike': pic_id in g.user.likes,
                'likes': pic.likes,
            })

        return {
            'msg': 'OK',
            'result': {
                'prefix': 'http://34.65.122.100:4000/img/',
                'pictures': pictures_result
            }
        }


like_fields = picture_api.model(
    'like', {
        'pic_id': fields.Integer(required=True, description='picture id'),
    })


@picture_api.route('/like')
@picture_api.header('Authorization', 'the authorization where the token is')
@picture_api.expect(user_auth_header_parser)
class PictureLike(Resource):
    @picture_api.doc('like', body=like_fields)
    @login_required()
    def post(self):

        json = request.get_json()

        if json['pic_id'] is None:
            raise Exception('pic_id is required.')

        pic_id = json['pic_id']

        result = user_like_a_pic(g.user, pic_id)
        current_app.logger.info('PictureLike post adjust the pic likes')
        change_likes_of_pic(pic_id, result)

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
@picture_api.header('Authorization', 'the authorization where the token is')
@picture_api.expect(user_auth_header_parser)
class PictureUpload(Resource):
    @picture_api.doc('upload', body=upload_fields)
    @login_required()
    def post(self):

        # once_load_all()

        # json = request.get_json()
        # """validate req data"""
        # error = None

        # if not json['name']:
        #     error = 'Name is required.'
        # if not json['img_url']:
        #     error = 'Image url is required.'
        # if not json['tags']:
        #     error = 'Tags field is required.'

        # if error is None:
        #     """service logic"""
        #     picture = upload(name=json['name'],
        #                      image=json['img_url'],
        #                      tags=json['tags'])
        #     print(picture.to_json())
        #     return {'msg': 'OK', 'result': picture.to_json()}

        # else:
        #     return {'msg': error}, 400

        return {'msg': 'OK'}
