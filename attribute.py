import random as R

def words(fn):
  with open(f'vocab/{fn}.txt', 'r') as f: txt = f.read()
  return txt.split('|')

grammar = ['NN', 'NS', 'AJ', 'BV']

V = dict()
for g in grammar: V[g] = words(g)

def W(g): return R.choice(V[g])

ATTR = [
  'NN', 'NN', 'NN', 
  'NS', 'NS', 'NS', 
  'AJ', 'AJ', 'AJ', 
  'BV AJ', 'BV AJ', 'BV AJ', 
  'BV a NN', 
  'BV a AJ NN', 
  'BV some NS', 
  'BV some AJ NS'
]

def attr():
  res = ''
  for LL in R.choice(ATTR).split(' '):
    if LL in grammar: res += f'{W(LL)} '
    else: res += f'{LL} '
  return res

if __name__ == '__main__':

  for i in range(10): print(attr())

  print(f'''
  some thing:
    ∙ {attr()}
    ∙ {attr()}
    ∙ {attr()}

  some other thing:
    ∙ {attr()}
    ∙ {attr()}
    ∙ {attr()}''')