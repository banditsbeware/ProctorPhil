import requests
import re

import os
from dotenv import load_dotenv
load_dotenv()
WORDNIK_KEY = os.getenv('WORDNIK_KEY')

class Words:
    
    # initialize with your api key
    def __init__(self, api_key):
        self.base = 'http://api.wordnik.com/v4'
        self.key = api_key

    # basic url builder for the words.json endpoint
    def get(self, command, args=[]):
        url = f'{self.base}/{command}?'
        for arg in args:
            url += arg + '&'
        url += f'api_key={self.key}'
        res = requests.get(url)
        status = res.status_code
        if status == 200: return res
        if status == 429: raise RuntimeError('429: too many requests.')
        url = url[:-len(self.key)] + '...'
        raise RuntimeError(f'wordnik returned status code {status} for the following URL:\n\t{url}')

        # a list of n random words
    def random(self, n=0):
        if n < 0: raise ValueError('Words.random(n): n must be zero or a positive integer')
        if n:
            json = self.get('words.json/randomWords', [f'limit={n}']).json()
            return [json[i]['word'] for i in range(n)]
        else:
            return self.get('words.json/randomWord').json()['word']

    def define(self, word, n):
        try:
            json = self.get(f'word.json/{word}/definitions').json()
            defs = []
            i = 0
            while len(defs) < n and i < len(json):
                if json[i].__contains__('text'): 
                    txt = json[i]['text']
                    txt = re.sub('<.*?>', '', txt)
                    defs.append(txt)
                i += 1
            return defs
        except RuntimeError:
            return None

if __name__ == '__main__':
    words = Words(WORDNIK_KEY)
    # print(words.random(10))
    w = words.random()
    print(f'{w}:')
    defs = words.define(w, 5)
    if defs:
        for d in defs:
            print(f'  - {d}')
        
