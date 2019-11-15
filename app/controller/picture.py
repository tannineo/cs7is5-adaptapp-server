from flask import request
from flask_restplus import Namespace, Resource, fields
from mongoengine.errors import ValidationError

from service.picture import get_by_tag, upload

picture_api = Namespace(
    'picture',
    description='Picture Controller, search, recommend, like and upload')

@picture_api.route('/search')
class PictureSearch(Resource):
    @picture_api.doc('search')
    def get(self):
        search_str = request.args.get("search")

        pictures = get_by_tag(search_str)
        if (pictures == None):
            return {'msg': '404', 'result': "No pictures found"}
        else:
            return {'msg': 'OK', 'result': {'picutres' : pictures.to_json()}}


@picture_api.route('/recommend')
class PictureRecommend(Resource):
    @picture_api.doc('recommend')
    def get(self):
        return {'msg': '404', 'result': "No pictures found"}

        # user = session.user
        # tags = recom
        # pictures = get_by_tag(search_str)
        # if (pictures == None):
        #     return {'msg': '404', 'result': "No pictures found"}
        # else:
        #     return {'msg': 'OK', 'result': pictures.to_json()}


upload_fields = picture_api.model(
    'upload', {
        'name': fields.String(required=True, description='name'),
        'img_url': fields.String(required=True,description='image url'),
        'tags': fields.List(cls_or_instance=fields.String,required=True, description='tags'),
    })



@picture_api.route('/upload')
class PictureUpload(Resource):
    @picture_api.doc('upload', body=upload_fields)
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