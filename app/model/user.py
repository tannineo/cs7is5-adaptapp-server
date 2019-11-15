import datetime

from constant import UserRole
from . import db


class User(db.Document):
    email = db.StringField(required=True)
    """MD5 password"""
    password = db.StringField(required=True)
    username = db.StringField(required=True, max_length=50)
    roles = db.ListField(db.StringField, default=lambda: [UserRole.USER])
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)
