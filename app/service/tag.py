from flask import current_app

from model.tag import Tag
from constant import TagRecommendRanking


# get system suggested initial tags
def get_initial_tag_list(number=10):
    tags = Tag.objects(recommended_ranking=TagRecommendRanking.STAR5.value)
    if len(tags) <= 0:
        tags = []
    else:
        tags = list(map(lambda t: t.name, tags))
    current_app.logger.info('get tag list:')
    current_app.logger.info(tags)

    return tags
