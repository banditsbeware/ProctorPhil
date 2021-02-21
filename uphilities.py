# Proctor Phil's utilities

import os
import re
import requests
import random as R

from dotenv import load_dotenv; load_dotenv()

from database import Database
db = Database(os.getenv('PATH_TO_DATABASE'))
attr_list = [
  
]
def compare(a, b):
  
  pass

re_li = re.compile('<li.*?>.*?(?=<ol>|</li>)')
def get_todo():
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
  return f'{R.randint(0, len(lis))}. {li}'

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

