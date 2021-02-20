# ProctorPhil

import os
import re
import quiz
import paul
import discord
import compare
from discord.ext import commands
from random import sample, choice, random
from homework import explanation, wikirand

from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

QUIZ = quiz.Quiz()

@bot.event
async def on_ready():
  print(f'{bot.user.name} has connected to {[bot.guilds[i].name for i in range(len(bot.guilds))]}')
  
"""
@bot.command(name='FunctionName', help='description')	
async def MyFunction(ctx):
   await ctx.send(SomeResponse)

"""

@bot.command(name='quiz', help='begins a new quiz')
async def quiz(ctx):
  print(f'{ctx.author.name} started a new quiz')
  QUIZ.clear_questions()

@bot.command(name='question', help='adds a question to the quiz and displays it to the chat')
async def question(ctx):
  print(f'{ctx.author.name} generated a question')
  new_question = QUIZ.add_question()
  await ctx.send(new_question.question_string())
  print(f'\tquiz now has {QUIZ.num_questions()} questions')

@bot.command(name='answer', help='submits your answer to a question')
async def quiz(ctx, ans, n=0):
  name = ctx.author.name

  if ans in ['A', 'B', 'C', 'D']:
    if n > QUIZ.num_questions():
      await ctx.send(f'The current quiz only has {QUIZ.num_questions()} questions.')
      return

    code = QUIZ.submit_answer(name, ans, n)

    if code == 2: 
      await ctx.send(f'Sorry, {name}, but that question is closed.')
      return
      
    if code == 1: 
      await ctx.send(f'Sorry, {name}, but only one attempt is allowed per question.')
      return
    
    QUIZ.save_grades()
    print(f'\t{name} submitted an answer to ' + ('the latest question' if n==0 else f'question {n}'))

@bot.command(name='explain', help='displays the explanation for a question and closes it')
async def quiz(ctx, n=0):
  name = ctx.author.name

  if n > QUIZ.num_questions():
    await ctx.send(f'The current quiz only has {QUIZ.num_questions()} questions.')
    return

  print(f'\t{name} motioned to explain ' + ('the latest question' if n==0 else f'{n}'))
  await ctx.send(QUIZ.find_question(n).get_explanation())

# method to randomize factabout() a little
def pref(sub):
  return choice([
    f'Here\'s a fact about {sub}:\n',
     'Hmmm... I think that ',
     'If I remember correctly, ',
     'It may surprise you, but ',
     'It turns out that ',
     'As a matter of fact, ',
    f'I have some experience with {sub}. ',
     'The evidence indicates that '
  ])
@bot.command(name='factabout', help='gives you a fact about something')
# asterisk to grab the whole list of space-separated args
async def factabout(ctx, *subject): 
  sub = ' '.join(subject).capitalize()

  # if nothing is entered, select a random page
  if len(sub) == 0: sub = wikirand()

  sub = f'**{sub}**'

  # send response
  print(f'{ctx.author.name} is learning about {sub[2:-2]}')
  await ctx.send(f'{pref(sub)}{explanation([sub])}')


@bot.command(name='talkabout', help='get Phil\'s thoughts about something')
async def comment(ctx, *topic):
  topic = ' '.join(topic)

  # search twitter for the given string
  comment = paul.simple_search(topic) if len(topic) else paul.simple_search()

  # get rid of links (not extensively tested but seems to work)
  comment = re.sub(' ??https?://.*/\w+ ??', '', comment)
  comment = re.sub('&amp;', '&', comment) # ... and fix ampersands

  # send response
  print(f'{ctx.author.name} wants to talk about {topic}')
  await ctx.send(comment)


c = compare.Comparer()
@bot.command(name='compare', help='list some pros and cons about two things (ex: \"compare dogs and cats\"')
async def compare(ctx, *args):
  args = ' '.join(args)

  if ' and ' not in args:
    await ctx.send('Format: /compare `thing 1` and `thing 2`')

  else:
    args = args.split(' and ')
    
    print(f'{ctx.author.name} compared {args[0]} and {args[1]}')
    await ctx.send(c.compare(args[0], args[1]))

@bot.command(name='aspire', help='what does Phil aspire to?')
async def aspire(ctx):
  base = choice(['i want', 'i need', 'i wish', 'i will', 'i have to'])
  await ctx.send(paul.simple_search(base))

import urbanpython
urban = urbanpython.Urban(os.getenv('URBAN_DICTIONARY_KEY'))
@bot.command(name='define', help='learn the definition of a word or phrase')
async def define(ctx, *args):

  # join arguments into one query
  query = ' '.join(args)
  result = urban.search(query)

  # chance to add example
  defn = result.definition + (f'\n\n{result.example}' if random() < 0.3 else '')

  # remove brackets etc.
  defn = re.sub(r'(\[|\]|\{|\})', '', defn)

  # send response
  print(f'{ctx.author.name} has defined \'{query}\' for the channel')
  await ctx.send(f'**{query}**: {defn}')

bot.run(TOKEN)
