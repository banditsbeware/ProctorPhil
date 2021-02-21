import sqlite3

VOCAB_CREATE = 'CREATE TABLE IF NOT EXISTS vocabulary (token TEXT UNIQUE, part TEXT)'
VOCAB_INSERT = 'INSERT OR REPLACE INTO vocabulary VALUES (?,?)'
VOCAB_SELECT = 'SELECT * FROM vocabulary WHERE part IS ?'

class Database:
  def __init__(self, path):
    self.conn = sqlite3.connect(path)
    self.conn.execute(VOCAB_CREATE)
    self.valid_parts = [
      'NOUN-DISCRETE',          # egg, dog, hat
      'NOUN-DISCRETE-PLURAL',   # eggs, dogs, hats
      'NOUN-CONTINUOUS',        # water, science, milk
      'VERB',                   # sing, die, exist
      'VERB-TRANSITIVE',        # punch, look at, think about
      'ARTICLE',                # the, my, his 
      'ADJECTIVE',              # blue, difficult, sour
      'ADVERB',                 # quickly, surprisingly
      'MISC'                    # oooOOOooooOOOoOOOoOoo
    ]

  def reset(self):
    self.conn.execute(f'DROP TABLE vocabulary')
    self.conn.commit()
    self.__init__(self.path)
  
  def fetch(self, part):
    if part not in self.valid_parts: 
      raise ValueError(f'database fetch failed\ninvalid part of speech: {part}')

    cur = self.conn.cursor()
    cur.execute(VOCAB_SELECT, (part,))
    return cur.fetchall()

  def insert(self, token, part):
    if part not in self.valid_parts:
      raise ValueError(f'database insert failed\ninvalid part of speech: {part}')

    if type(token) is list:
      # create a list of tuples, e.g.
      # [('word 1', 'NOUN'), ('word 2', 'NOUN'), ('word 3', 'NOUN'),...]
      values = [(i, part) for i in token]
    else:
      values = (token, part)

    self.conn.execute(VOCAB_INSERT, values)
    self.conn.commit()

  def count(self, part):
    if part not in self.valid_parts:
      raise ValueError(f'database count failed\ninvalid part of speech: {part}')
    return len(self.fetch(part))

  def summary(self):
    for part in self.valid_parts:
      print(f'{part}: {self.count(part)}')


if __name__ == '__main__':
  
  db = Database('./vocabulary.db')

  db.summary()