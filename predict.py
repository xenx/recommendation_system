"""
Get predictions by ids of user's news
"""
from data.data_utils import TvrainData
from models import random_model

model = random_model
model.init()


def predict(first_id=None, second_id=None, third_id=None,
            tvrain_data=None, recommends_num=3):
    """
    Get news predictions. If one of ids isn't specified,
    so replace it to most popular articles. If none of ids
    is specified, get most popular news.
    :param first_id: MongoDB id of first article
    :param second_id:
    :param third_id:
    :param tvrain_data: data.data_utils.TvrainData object
    :param recommends_num: num of articles to recommend
    :return: [{'id': '', 'url': '', 'title': ''}, ...]
    """
    input_ids = [first_id, second_id, third_id]
    input_articles = tvrain_data.get_articles_data([
        first_id, second_id, third_id
    ])
    result = model.predict(
        input_articles=input_articles,
        input_ids=input_ids,
        tvrain_data=tvrain_data,
        recommends_num=recommends_num
    )
    # TODO: Follow return format
    return result
