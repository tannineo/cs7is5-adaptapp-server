from flask import request, g
from flask_restplus import Namespace, Resource, fields
from mongoengine.errors import ValidationError

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
            return {'msg': '400', 'result': "Please include a tag to search"}

        pictures = get_by_tag(search_str)
        if (pictures == None):
            return {'msg': '404', 'result': "No pictures found"}
        else:
            return {'msg': 'OK', 'result': {'picutres' : pictures.to_json()}}


@picture_api.route('/recommend')
class PictureRecommend(Resource):
    @picture_api.doc('recommend')
    @login_required()

    def get(self):
        return {'msg': '404', 'result': "No pictures found"}

        # user = session.user
        # tags = recom
        # pictures = get_by_tag(search_str)
        # if (pictures == None):
        #     return {'msg': '404', 'result': "No pictures found"}
        # else:
        #     return {'msg': 'OK', 'result': pictures.to_json()}

@picture_api.route('/like')
class PictureLike(Resource):
    @picture_api.doc('like')
    @login_required()

    def post(self):
        return {'msg': "x"}, 400

        json = request.get_json()

        """validate req data"""
        error = ''

        if not json['pic_id']:
            error = 'pic_id is required.'
        
        if error is '':
            pic_id = json['pic_id']
            picture = Picture.objects(id=pic_id)

            user = g.user
            user.update(push__likes=picture)
            

        else:
            return {'msg': error}, 400


upload_fields = picture_api.model(
    'upload', {
        'name': fields.String(required=True, description='name'),
        'img_url': fields.String(required=True,description='image url'),
        'tags': fields.List(cls_or_instance=fields.String,required=True, description='tags'),
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