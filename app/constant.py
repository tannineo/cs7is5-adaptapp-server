from enum import Enum


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class ForcePicConfig(Enum):
    DEFAULT = 'default'
    BIG = 'big'
    SMALL = 'small'


class TagRecommendRanking(Enum):
    STAR1 = 1
    STAR2 = 2
    STAR3 = 3
    STAR4 = 4
    STAR5 = 5
