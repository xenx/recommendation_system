from collections import Counter
import random


def init():
    pass


def predict(input_articles, input_ids, tvrain_data, recommends_num):
    result_counter = Counter()
    for article in tvrain_data.iterate_articles(except_articles=input_ids):
        result_counter[article['_id']] = random.random()
    return list(result_counter.most_common(recommends_num))
