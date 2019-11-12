from . import db
import datetime


class User(db.Document):
    email = db.StringField(required=True)
    """MD5 password"""
    password = db.StringField(required=True)
    username = db.StringField(required=True, max_length=50)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)
