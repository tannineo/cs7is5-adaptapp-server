from . import db
import datetime


class Picture(db.Document):
    name = db.StringField(required=True)
    img_url = db.StringField(required=True)
    tags = db.ListField(db.StringField(max_length=50))
    likes = db.IntField(default=0)
