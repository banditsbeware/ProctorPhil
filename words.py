import requests
import os

from dotenv import load_dotenv
load_dotenv()

url = "https://wordsapiv1.p.rapidapi.com/words/"
headers = {
  'x-rapidapi-key': os.getenv('WORDS_KEY'),
  'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
}

def rand():
  json = requests.get(url, headers=headers, params={'random':'true'}).json()
  return json['word']

def verb():
  json = requests.get(url, headers=headers, params={'partOfSpeech':'verb', 'limit':'1000', 'page':'5'}).json()
  return json


if __name__ == '__main__':

  print(rand(10))