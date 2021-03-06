import datetime
import json
import os
import pytz
import tweepy
from tweeter_key import *


class Model:

  def __init__(self, unique_id, text, author, created_at, lang, favorite_count):
    self.text = text
    self.author = author
    self.created_at = created_at
    self.lang = lang
    self.favorite_count = favorite_count
    self.unique_id = unique_id


class ModelEncoder(json.JSONEncoder):

  def default(self, obj):
    if isinstance(obj, Model):
      return {"id": obj.unique_id,
              "text": obj.text,
              "author": obj.author,
              "created_at": obj.created_at,
              "lang": obj.lang,
              "favorite_count": obj.favorite_count}
    # Let the base class default method raise the TypeError
    return json.JSONEncoder.default(self, obj)


def crawl(name, store=False):
  print 'crawling', name, 'tweeter timeline'

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  result = []
  api = tweepy.API(auth)
  i = 1

  while True:
    print 'crawling page', i, 'of', name

    tweets = api.user_timeline(name, count=200, page=i)

    for tweet in tweets:
      unique_id = tweet.id
      text = tweet.text
      author = tweet.author.name
      created_at = tweet.created_at.isoformat() + 'Z'
      lang = tweet.lang
      favorite_count = tweet.favorite_count

      data = Model(unique_id, text, author, created_at, lang, favorite_count)
      result.append(data)

    i += 1
    print 'crawled', len(tweets), 'tweets'

    if len(tweets) == 0:
      break

  result_json = json.dumps(result, cls=ModelEncoder)

  if store:
    if not os.path.exists('data/'):
      os.makedirs('data/')

    f = open('data/' + name + '_data.json', 'w')
    f.write(result_json)
    f.close()

  return result_json


if __name__ == "__main__":
  crawl('espn', store=True)
  crawl('TheNBACentral', store=True)
  crawl('SimpleNBAScores', store=True)
  crawl('ESPNNBA', store=True)
  crawl('NBATV', store=True)
