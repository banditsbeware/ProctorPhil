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
  text = R.choice(tweets)['full_text']
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

from attribute import attr
def a():
  p = R.random()
  if p < 0.7: return attr()
  if p < 0.9: return random_word()
  return get_todo()

def compare(x, y):
  result = f'**{x}**:\n'
  for i in range(R.randint(1,4)):
    result += f' ∙ {a()}\n'
  
  result += f'\n**{y}**:\n'
  for i in range(R.randint(1,4)):
    result += f' ∙ {a()}\n'

  return result


import shutil
img_src_RE = re.compile('(?<=\sdata-src=").*?(?=")')
img_alt_RE = re.compile('(?<=\salt=").*?(?=")')
def image(query=None, mime=None):
  # build request URL
  url = 'https://commons.wikimedia.org/w/index.php?search='

  if query is None:
    url += random_word()
  else:
    url += query.replace(' ', '+')

  url += '&title=Special:MediaSearch&go=Go&type=image'

  # filter by file type (.png, .gif, etc)
  if mime is not None: url += f'&filemime={mime}'

  # entire results page HTML
  html = requests.get(url).text

  imgs = img_src_RE.findall(html)       # all image URLs  
  alts = img_alt_RE.findall(html)[:-4]  # associated alt text

  # no images found - try a random query
  if len(imgs) == 0: return image(mime=mime)

  img_number = R.randint(0, len(imgs)-1)

  aboutstr = alts[img_number]
  imageurl = imgs[img_number]

  return imageurl, aboutstr

genre_url = 'https://binaryjazz.us/wp-json/genrenator/v1/genre/'
genre_comments = [
  'That sounds like _.', 'That\'s some good _.', 'banger', 'this slaps', 'this smacks',
  'I can\'t tell if that\'s _ or _.', 'This is the intersection of _ and _.',
  'This redefines _.', 'I love _.', 'Thank you for sharing some classic _.', 'Jamming rn',
  '_-type beat', '_ vibes', 'My mother also listens to _.']
def music_comment():
  comment = R.choice(genre_comments)
  while comment.find('_') >= 0:
    comment = comment.replace('_', requests.get(genre_url).text, 1)
  comment = comment.replace('"', '*')
  comment = comment.replace('\\', '')
  return comment

num_quote_sources = 3
def quote():
  if R.random() < 1/num_quote_sources: return general_quote()
  if R.random() < 1/num_quote_sources: return kanye_quote()
  if R.random() < 1/num_quote_sources: return anime_quote()
  return quote()

def general_quote(proper=False):
  json = requests.get('https://api.fisenko.net/quotes?l=en').json()
  return f'"{json["text"]}"\n - {json["author"]}' if proper else json['text']

def kanye_quote():
  return requests.get('https://api.kanye.rest?format=text').json()['quote']

def anime_quote():
  return requests.get('https://animechan.vercel.app/api/random').json()['quote']

def shuffle_text(string):
  words = string.split(' ')
  R.shuffle(words)
  return ' '.join(words)

from PIL import Image
def blend_images(path1, path2):
  img1 = Image.open(path1)
  img2 = Image.open(path2).resize(img1.size)
  img2.convert(img1.mode)

  destfn = './img/blend.png'
  Image.blend(img1, img2, 0.5).save(destfn)

from png import *
def edit(path):

  im = Image.open(path)

  for _ in range(15):
    R.choice(FUNCTIONS)(im)
  im.save('./img/edit.png')
  return False

emlist = ['😀', '😖', '👏', '🍆💦', '😬', '😔', '😞', '🙌', '💪', '🙏', '👀', '🗣', '👌', '😭', '😉', '😋', '🙇', '💫', '🔥', '✨', '™️', '🌈', '📈', '❤', '🅱', '💯', '💭', '😷', '😓', '😳', '😍', '™️', '♿️', '❌']
def random_emoji():
  return R.choice(emlist) + ' '

def emojify(text):

  text = text.split(' ')

  res = ''

  for word in text:

    if R.random() < 0.5: 
      res += random_emoji()
      if R.random() < 0.5: 
        res += random_emoji()
        if R.random() < 0.5: 
          res += random_emoji()

    res += word + ' '

  return res

if __name__ == '__main__':
  print(emojify('hey jackie, this is a cool idea!'))