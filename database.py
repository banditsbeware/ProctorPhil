import sqlite3
class Database:
  def __init__(self, _path):
    self.path = _path
    self.speech = ['noun', 'nounplural', 'nouncont', 'art1', 'art2', 'verb', 'verbs', 'verbing', 'adjective', 'adverb']
    for part in self.speech:
      self.execute(f'CREATE TABLE IF NOT EXISTS {part} (token text unique)')

  def reset(self, part=None):
    if part is None:
      for p in self.speech:
        self.execute(f'DROP TABLE {p}')
    else:
      self.execute(f'DROP TABLE {part}')

    self.__init__(self.path)
  
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

  def summary(self):
    for part in self.speech:
      print(f'{part}: {self.count(part)}')


if __name__ == '__main__':
  
  db = Database('./vocabulary.db')

  db.summary()