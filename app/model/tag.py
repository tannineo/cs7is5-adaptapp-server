import datetime

from constant import TagRecommendRanking
from . import db


class Tag(db.Document):
    name = db.StringField(required=True, unique=True)
    recommended_ranking = db.IntField(
        required=True, default=lambda: TagRecommendRanking.STAR1)
    create_time = db.DateTimeField(default=datetime.datetime.utcnow)
