from random import randint as ri
from random import random as r
from random import sample
import paul
from database import Database

def lexicon():
  f = open('thing.txt', 'r')
  lex = f.read().split('\n')
  for l in range(len(lex)):
    lex[l] = lex[l].split(' ')
  
  for l in range(len(lex)):
    lex[l] = [lex[l][i].replace('_',' ') for i in range(len(lex[l]))]
    
  f.close()
  return lex

class Comparer:

  def __init__(self):
    self.lex = lexicon()
    self.db = Database()

  def grab(self, b):
    s = ''
    for w in b:
      if w == 6 or w == 7 or w == 8:
        if r() < 0.7: continue
      s += (sample(self.lex[w][1:], 1)[0] + ' ')
    return s

  def item(self, subj=None):
    x = ri(0,2)
    if subj is None: subj = self.grab([x])

    subj = f'**{subj}**:\n\n'

    for i in range(ri(1,4)):
      subj += (' - ' + self.attribute(subj) + '\n')

    return subj

  def attribute(self, subj):
    if r() < 0.3:
      return self.grab([6,5,8,ri(0,1)])
    if r() < 0.4:
      return f'{self.db.random("noun")}'
    if r() < 0.4:
      return f'{self.db.random("verb")} {self.db.random("noun")}'
    if r() < 0.4:
      return self.grab([6,9])+'and '+self.grab([9])
    if r() < 0.4:
      return paul.random_word()
    if r() < 0.4:
      return self.grab([3])

    return paul.simple_search(subj)

  def compare(self, a, b):
    return f'\n{self.item(a)}\n{self.item(b)}'


if __name__ == '__main__':
  c = Comparer()
  print(c.compare('bats', 'cats'))




















