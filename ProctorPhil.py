# ProctorPhil

import os
import re
import discord
import random as R
from discord.ext import tasks, commands

import uphilities as phil

from dotenv import load_dotenv; load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

def log(msg):
  print(f'[Phil] {msg}')

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

  if R.random() < 0.05:
    quote = phil.quote()
    if R.random() < 0.3: quote = phil.shuffle_text(quote)
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

# method to randomize factabout() a little
def pref(sub):
  return R.choice([
    f'Here\'s a fact about {sub}:\n', 'Hmmm... I think that ',
     'If I remember correctly, ', 'It may surprise you, but ',
     'It turns out that ', 'As a matter of fact, ',
    f'I have some experience with {sub}. ', 'The evidence indicates that '
  ])
@bot.command(name='factabout', help='gives you a fact about something')
# asterisk to grab the whole list of space-separated args
async def factabout(ctx, *, arg): 
  # use wikitools via uphilities
  await ctx.reply('please tell david to fix this.')

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

with open('vocab/faces.txt', 'r', encoding='utf-8') as f: faces = f.read().split('\n')
@bot.command(name='mood', help='a big vibe')
async def mood(ctx):
  g = ctx.guild
  c = g.get_channel(806679944305311768)
  await c.edit(name=R.choice(faces))

ACROS = ['BRB', 'TTYL', 'LMAO', 'LOL', 'YOLO', 'OMG']
@bot.command(name='acro', help='add an acronym definition')
async def acro(ctx, acr, *, args):

  if acr not in ACROS:
    await ctx.reply(f'that acronym isn\'t on the list.', mention_author=False)
    return

  # this algorithm could be quite a lot better
  i = 0; j = 0
  while i < len(args) and j < len(acr):
    if args[i] == acr[j]: j += 1
    i += 1

  if j == len(acr):
    with open(f'vocab/acro_{acr}.txt', 'a') as f: f.write(f'{args}\n')
    await ctx.send(f'definition for {acr} added') 
  else:
    await ctx.send(f'that definition doesn\'t match') 

if __name__ == '__main__':
  bot.run(DISCORD_TOKEN)
