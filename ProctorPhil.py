# ProctorPhil

import os
import re
import quiz
import discord
from discord.ext import tasks, commands
from random import sample, choice, random
from homework import explanation, wikirand

import uphilities as phil

from dotenv import load_dotenv; load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

def log(msg):
  print(f'[Phil] {msg}')

QUIZ = quiz.Quiz()

# change Phil's presence to a todo item every hour
@tasks.loop(seconds = 60 * 60)
async def update_presence():
  doing = phil.get_todo()
  await bot.change_presence(activity=discord.Game(name=doing))
  log(f'Playing {doing}')

@bot.event
async def on_ready():
  log(f'logged in as {bot.user}')
  update_presence.start()

@bot.event
async def on_message(message):
    
  if message.author.bot: return

  msg = message.content

  # judge people's music suggestions in the music channel
  if message.channel.id == 817974358060040222:
    if re.search('://(open.spotify.com|youtu.be|www.youtube.com)/', msg) is not None:
      await message.channel.send(phil.music_comment())

  if random() < 0.05:
    quote = phil.quote()
    if random() < 0.3: quote = phil.shuffle_text(quote)
    await message.channel.send(quote)

  await bot.process_commands(message)

@bot.command(name='blend', help='blend some images')
async def blend(ctx):
  images_saved = 0
  img1, img2 = None, None

  # look for images in the most recent 50 messages
  async for msg in ctx.history(limit=50):

    # only consider messages from the issuer of this /blend command
    if msg.author == ctx.author:

      # look for an image in the message
      if len(msg.attachments) == 1 and msg.attachments[0].content_type.find('image') == 0:

        att = msg.attachments[0]
        imgpath = f'./img/{att.filename}'

        if images_saved == 0: img1 = imgpath
        if images_saved == 1: img2 = imgpath
        if images_saved == 2: break

        # download image
        await att.save(imgpath)

        images_saved += 1
  
  if img1 is None or img2 is None:
    ctx.send('Please send some images.')

  else:
    try:
      phil.blend_images(img1, img2)
      f = discord.File('./img/blend.png')
      e = discord.Embed(title=f'BLEND{img1}{img2}')
      e.set_image(url='attachment://img/blend.png')

      await ctx.send(file=f)

      for f in os.listdir('./img/'):
        os.remove(f'./img/{f}')

    except ValueError as e:
      await ctx.send(f'something\'s wrong with those images.\n\n`{e}`')

@bot.command(name='edit', help='edit an image')
async def edit(ctx):
  img = None 

  # look for images in the most recent 20 messages
  async for msg in ctx.history(limit=20):

    # only consider messages from the issuer of this /edit command
    if msg.author == ctx.author:

      # look for an image in the message
      if len(msg.attachments) == 1:# and msg.attachments[0].content_type.find('image') == 0:

        att = msg.attachments[0]
        img = f'./img/{att.filename}'
        break

  # download image
  if img is not None:
    await att.save(img)
    phil.edit(img)
  else:
    await ctx.reply('I couldn\'t find an image from you.', mention_author=False)

  f = discord.File(f'./img/edit.png')

  await ctx.send(file=f)

  for f in os.listdir('./img/'):
    os.remove(f'./img/{f}')

image_types = ['tiff', 'png', 'gif', 'jpg', 'webp', 'xcf', 'svg']
@bot.command(name='image', help='obtain one image')
async def image(ctx, *args):
  mime = None
  if len(args) > 0 and args[-1] in image_types:
    mime = args[-1]
    args = args[:-1]
  
  query = ' '.join(args) if len(args) > 0 else None
  url, desc = phil.image(query, mime)

  embed = discord.Embed(title=query, description=desc, url=url)
  embed.set_image(url=url)

  log(f'{ctx.author.name} wants a picture of {query if query is not None else "..."}')
  await ctx.reply(embed=embed, mention_author=False)

@bot.command(name='quote', help='wisdom from the masters')
async def quote(ctx):
  await ctx.reply(phil.general_quote(proper=True), mention_author=False)

@bot.command(name='quiz', help='begins a new quiz')
async def quiz(ctx):
  log(f'{ctx.author.name} started a new quiz')
  QUIZ.clear_questions()

@bot.command(name='question', help='adds a question to the quiz and displays it to the chat')
async def question(ctx):
  log(f'{ctx.author.name} generated a question')
  new_question = QUIZ.add_question()
  await ctx.send(new_question.question_string())
  log(f'quiz now has {QUIZ.num_questions()} questions')

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
    log(f'\t{name} submitted an answer to ' + ('the latest question' if n==0 else f'question {n}'))

@bot.command(name='explain', help='displays the explanation for a question and closes it')
async def quiz(ctx, n=0):
  name = ctx.author.name

  if n > QUIZ.num_questions():
    await ctx.send(f'The current quiz only has {QUIZ.num_questions()} questions.')
    return

  log(f'\t{name} motioned to explain ' + ('the latest question' if n==0 else f'{n}'))
  await ctx.send(QUIZ.find_question(n).get_explanation())

# method to randomize factabout() a little
def pref(sub):
  return choice([
    f'Here\'s a fact about {sub}:\n', 'Hmmm... I think that ',
     'If I remember correctly, ', 'It may surprise you, but ',
     'It turns out that ', 'As a matter of fact, ',
    f'I have some experience with {sub}. ', 'The evidence indicates that '
  ])
@bot.command(name='factabout', help='gives you a fact about something')
# asterisk to grab the whole list of space-separated args
async def factabout(ctx, *, arg): 
  sub = arg.capitalize()

  # if nothing is entered, select a random page
  if len(sub) == 0: sub = wikirand()

  sub = f'**{sub}**'

  # send response
  log(f'{ctx.author.name} is learning about {sub[2:-2]}')
  await ctx.reply(f'{pref(sub)}{explanation([sub])}', mention_author=False)

@bot.command(name='talkabout', help='get Phil\'s thoughts about something')
async def comment(ctx, *, topic):
  # search twitter for the given string
  comment = phil.twitter_search(topic) if len(topic) else phil.twitter_search()

  # send response
  log(f'{ctx.author.name} wants to talk about {topic}')
  await ctx.reply(comment, mention_author=False)

@bot.command(name='compare', help='list some pros and cons about two things (ex: \"compare dogs and cats\"')
async def compare(ctx, *, args):
  # ensure argument has the correct format
  if ' and ' not in args:
    await ctx.reply('Format: /compare `thing 1` and `thing 2`', mention_author=False)

  # this way, phil can compare things that have more than one word
  # as in "/compare my mom and your mom"
  else:
    args = args.split(' and ')
    
    log(f'{ctx.author.name} compared {args[0]} and {args[1]}')
    await ctx.reply(phil.compare(args[0], args[1]), mention_author=False)

@bot.command(name='define', help='learn the definition of a word or phrase')
async def define(ctx, *, query):
  if len(query) > 0:
    log(f'{ctx.author.name} has defined \'{query}\' for the channel')
    await ctx.reply(f'**{query}**: {phil.urban_definition(query)}', mention_author=False)

@bot.command(name='todo', help='get an item from the Post-Quarantine Bucket List')
async def todo(ctx):
  log(f'{ctx.author.name} needs something to do...')
  await ctx.reply(phil.get_todo(with_number=True), mention_author=False)

if __name__ == '__main__':
  bot.run(DISCORD_TOKEN)
