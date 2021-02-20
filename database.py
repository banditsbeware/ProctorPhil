import os
import sqlite3
from random import choice

from dotenv import load_dotenv; load_dotenv()

class Database:
  def __init__(self):
    self.path = os.getenv('PATH_TO_DATABASE')
    self.speech = ['noun', 'verb', 'adjective', 'adverb']
    for part in self.speech:
      self.execute(f'CREATE TABLE IF NOT EXISTS {part} (token text unique)')

  def reset(self):
    for part in self.speech:
      self.execute(f'DROP TABLE {part}')
    self.__init__()
  
  def execute(self, operation):
    conn = sqlite3.connect(self.path)
    conn.execute(operation)
    conn.commit()
    conn.close()
  
  def fetch(self, part):
    cur = sqlite3.connect(self.path).cursor()
    cur.execute(f'SELECT * FROM {part}')
    return [token[0] for token in cur.fetchall()]

  def insert(self, part, word):
    if part not in self.speech:
      raise ValueError(f'Invalid part of speech: {part}')
    if type(word) is list:
      for w in word:
        self.execute(f'INSERT OR REPLACE INTO {part} (token) VALUES (\'{w}\');')
    else:
      self.execute(f'INSERT OR REPLACE INTO {part} (token) VALUES (\'{word}\');')

  def count(self, part):
    return len(self.fetch(part))

  def random(self, part):
    return choice(self.fetch(part))
  
  def summary(self):
    for part in self.speech:
      print(f'{part}: {self.count(part)}')

if __name__ == '__main__':
  db = Database()

  part = 'verb'
  blob = ''
  if len(blob):
    db.insert(part, blob.split('\n'))

  print(db.random('noun'))
  db.summary()