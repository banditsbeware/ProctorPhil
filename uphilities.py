# Proctor Phil's utilities

import os
import re
import requests
import random as R

from dotenv import load_dotenv; load_dotenv()

# wordnik allows unlimited requests, but will 429 pretty quickly
# .. in that case, use wordsAPI
wordnik_url = os.getenv('WORDNIK_URL')
words_url = f'https://wordsapiv1.p.rapidapi.com/words/'
words_headers = { 'x-rapidapi-key': os.getenv('WORDS_KEY'), 
  'x-rapidapi-host': 'wordsapiv1.p.rapidapi.com' }
def random_word():
  wordnik_resp = requests.get(wordnik_url)
  if wordnik_resp.status_code == 200:
    return wordnik_resp.json()['word']

  words_resp = requests.get(words_url, headers=words_headers, params={'random':'true'})
  return words_resp.json()['word']


# return a tweet's text, obtained by searching for 'query'
from twython import Twython
twitter = Twython(os.getenv('TW_APP_KEY'),   os.getenv('TW_APP_SEC'),
                  os.getenv('TW_OAUTH_KEY'), os.getenv('TW_OAUTH_SEC'))
def twitter_search(query=None):
  if query is None: query = random_word()

  # make request to twitter
  query += ' -filter:retweets -filter:replies'
  tweets = twitter.search(q=query, tweet_mode='extended', lang='en')['statuses']

  # if no tweets are found, search for a random word instead
  if len(tweets) == 0: return twitter_search()

  # choose a random result and clean text
  text = R.choice(tweets)['full-text']
  text = re.sub(' ??https?://.*/\w+ ??', '', text)
  text = re.sub('&amp;', '&', text)

  return text

re_li = re.compile('<li.*?>.*?(?=<ol>|</li>)')
def get_todo(with_number=False):
  # ask the bucket list for its items
  with requests.get('https://pigeon.dog') as res:
    if res.status_code != 200:
      raise RuntimeError(f'request to PQBL returned status code {res.status_code}')
    # the raw html string
    html = str(res.text)     

  # pick a list item
  lis = re_li.findall(html)
  li = R.choice(lis)

  # clean out the junk and format for discord
  li = re.sub('<b.*?>|</b>', '**', li)
  li = re.sub('<em.*?>|</em>', '*', li)
  li = re.sub('<u.*?>|</u>', '__', li)
  li = re.sub('<code.*?>|</code>', '`', li)
  li = re.sub('&emsp;', '    ', li)
  li = re.sub('<.*?>', '', li)

  # return a random number with the list item
  return f'{R.randint(0, len(lis))}. {li}' if with_number else li

import urbanpython
urban = urbanpython.Urban(os.getenv('URBAN_DICTIONARY_KEY'))
def urban_definition(query):
  # search Urban Dictionary for query
  result = urban.search(query)
  # add example
  defn = f'{result.definition}\n\n{result.example}'
  # remove brackets etc
  defn = re.sub(r'(\[|\]|\{|\})', '', defn)
  return defn

from database import Database
db = Database(os.getenv('PATH_TO_DATABASE'))
def attr(thing):
  if R.random() < 0.075:
    return get_todo()

  if R.random() < 0.2:
    return f"is a {db.random('ADVERB')} {db.random('ADJECTIVE')} {db.random('NOUN-DISCRETE')}"

  if R.random() < 0.5:
    return f"{db.random('VERB-HELPER')} {db.random('VERB')}"

  if R.random() < 0.5:
    return f"{db.random('VERB-HELPER')} {db.random('VERB-TRANSITIVE')} {db.random('ARTICLE')} {db.random('NOUN-DISCRETE')}"
  
  if R.random() < 0.5:
    return f"{db.random('VERB-HELPER')} {db.random('VERB-TRANSITIVE')} {db.random('ARTICLE')} {db.random('NOUN-CONTINUOUS')}"

  return db.random('MISC')

def compare(a, b):
  result = f'**{a}**:\n'
  for i in range(R.randint(1,3)):
    result += f' ∙ {attr(a)}\n'
  
  result += f'\n**{b}**:\n'
  for i in range(R.randint(1,3)):
    result += f' ∙ {attr(b)}\n'

  return result



