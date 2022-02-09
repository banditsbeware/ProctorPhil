from discord.ext import commands
from random import random, choice, randint
from utils import *

def words(fn):
  with open(f'vocab/{fn}.txt', 'r') as f: txt = f.read()
  return txt.split('|')

grammar = ['NN', 'NS', 'AJ', 'BV']

V = dict()
for g in grammar: V[g] = words(g)

def W(g): return choice(V[g])

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

# TODO: more vocabulary and functions to choose from !
def attr():
  res = ''
  for LL in choice(ATTR).split(' '):
    if LL in grammar: res += f'{W(LL)} '
    else: res += f'{LL} '
  return res

funcs = [ attr, todo, random_word ]
def list_attributes(v):
  result = ''
  for item in v:
    result += f'**{item}**:\n'
    for i in range(randint(1,4)):
      result += f'  ∙ { choice(funcs)() }\n'
    result += '\n'

  return result

class Attribute(commands.Cog, name='Attribute'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='compare')
  async def compare(self, ctx, *, args):
    # phil can compare things that have more than one word
    # as in "/compare my mom and your mom"
    args = args.split(' and ')
    
    with ctx.typing():
      await ctx.send(list_attributes(args))


def setup(bot):
  bot.add_cog(Attribute(bot))