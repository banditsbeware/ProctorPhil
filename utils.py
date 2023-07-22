import json
import requests
import regex as re
from random import choice

with open('./config.json', 'r') as f: config = json.load(f)

def clean_tags(t):
  t = re.sub(r'<i.*?>|</i>', '*', t)
  t = re.sub(r'<b.*?>|</b>', '**', t)
  t = re.sub(r'<.*?>', '', t)
  t = re.sub(r'&amp;', '&', t)
  t = re.sub(r'&emsp;', '    ', t)
  return t


item_re = re.compile(r'(?<=li.*?>)[\s\S]+?(?=</li>|<ol)')
def todo():
  html = requests.get('https://pigeon.dog').text
  all_items = item_re.findall(html)
  td = re.sub('<.*?>|&emsp;', '', choice(all_items))
  return td.strip() if len(td) > 0 else todo()


def random_word():
# res = requests.get(config['wordnik_url'])
# if res.status_code == 200:
#   return res.json()['word']

  t = requests.get('http://en.wikipedia.org/wiki/Special:Random').text
  t = clean_tags(t)
  T = list(set(t.split()))
  word = choice(T)
  while '.' in word:
    word = choice(T)
  return word


if __name__ == '__main__': 
  for _ in range(50):
    print(random_word())
