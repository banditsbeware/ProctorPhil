import os
import re
from random import choice
from twython import Twython
import pynik
from words import rand

from dotenv import load_dotenv
load_dotenv()
APP_KEY   = os.getenv('TW_APP_KEY')
APP_SEC   = os.getenv('TW_APP_SEC')
OAUTH_KEY = os.getenv('TW_OAUTH_KEY')
OAUTH_SEC = os.getenv('TW_OAUTH_SEC')

# cheap and unlimited random words, but 429 is pretty sensitive
wordnik = pynik.Words(os.getenv('WORDNIK_KEY'))

paul = Twython(APP_KEY, APP_SEC, OAUTH_KEY, OAUTH_SEC)
paul.verify_credentials()

def random_word():
  try:
    return wordnik.random()
  except RuntimeError:
    return rand()

def simple_search(term=None, n=1):

  if term is None:
    term = random_word()
    
  query = term + ' -filter:retweets -filter:replies'
  tweets = paul.search(q=query, tweet_mode='extended', lang='en')['statuses'][:n]

  if len(tweets) == 0:
    return simple_search()
  if len(tweets) == 1:
    return re.sub(' ??https?://.*/\w+ ??', '', choice(tweets)['full_text'])
  if len(tweets) > 1:
    return [re.sub(' ??https?://.*/\w+ ??', '', tweet['full_text']) for tweet in tweets]

if __name__ == '__main__':
  print(simple_search())
