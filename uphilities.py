# Proctor Phil's utilities

import os
import re
import requests
import random as R

from dotenv import load_dotenv; load_dotenv()

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

if __name__ == '__main__':
  print(compare('bananas', 'my mom'))


