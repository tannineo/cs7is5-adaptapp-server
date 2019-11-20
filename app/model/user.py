import datetime

from model.picture import Picture

from constant import UserRole, ForcePicConfig
from . import db


class User(db.Document):
    email = db.StringField(required=True, unique=True)

    # MD5 password
    password = db.StringField(required=True)
    username = db.StringField(required=True, max_length=50, unique=True)

    # user roles
    roles = db.ListField(db.StringField(), default=[UserRole.USER.value])

    # user prefered tags
    tags = db.ListField(db.StringField(), default=[])

    # force settings
    force_pic_config = db.StringField(default=ForcePicConfig.DEFAULT.value)

    create_time = db.DateTimeField(default=datetime.datetime.utcnow)

    likes = db.ListField(db.ReferenceField(Picture))
