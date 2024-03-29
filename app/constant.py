from enum import Enum


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class TagRecommendRanking(Enum):
    STAR1 = 1
    STAR2 = 2
    STAR3 = 3
    STAR4 = 4
    STAR5 = 5


class UserNetworkSetting(Enum):
    UNKNOWN = 'unknown'
    G2 = '2g'
    G3 = '3g'
    G4 = '4g'


# judge if a value is in a Enum
def isInEnum(value, enumerate: Enum):
    values = tuple(item.value for item in enumerate)
    if value in values:
        return True
    return False
