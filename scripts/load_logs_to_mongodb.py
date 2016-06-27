import os
import sys
from datetime import datetime
from collections import defaultdict
from pymongo import MongoClient

logs_file = open(sys.argv[1])
article_urls = set()
article_views = defaultdict(list)  # article_url: list of user's id's
article_times = {}
for line in logs_file:
    try:
        timestamp, url, user = line.strip().split('\t')
    except IndexError:
        continue
    timestamp = timestamp.strip(' GET').strip('Z')
    # Delete ms from timestamp
    timestamp = ''.join(timestamp.split('.')[:-1])
    event_time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    if not url or not user:
        continue
    if not url.startswith('https://tvrain.ru/'):
        continue
    article_urls.add(url)
    article_views[url].append(user)
    # Save time of only first event
    if url not in article_times:
        article_times[url] = event_time

mongodb_client = MongoClient(os.environ['MONGODB_URL'])
db = mongodb_client.tvrain
parsed_articles = db.tvrain
articles = db.articles
# Clear articles
articles.remove({})

for article in parsed_articles.find():
    if article['url'] not in article_urls:
        continue
    views = article_views[article['url']]
    compressed_views = []
    # Save only every 10th view
    for i in range(len(views)):
        if i % 10 == 0:
            compressed_views.append(views[i])
    articles.insert_one({
        '_id': article['_id'],
        'title': article['title'],
        'text': article['text'],
        'views': compressed_views,
        'time': article_times[article['url']]
    })

