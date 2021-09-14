# ProctorPhil

import os
import re
import discord
import random as R
from discord.ext import tasks, commands

import phutil as ph

from dotenv import load_dotenv; load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/')

def log(msg):
  print(f'[Phil] {msg}')

with open('vocab/faces.txt', 'r', encoding='utf-8') as f: faces = f.read().split('\n')

# change Phil's presence to a todo item every hour
@tasks.loop(seconds = 60 * 60)
async def update_presence():
  doing = ph.get_todo()
  g = bot.guilds[0]
  c = g.get_channel(806679944305311768)
  # await c.edit(name=R.choice(faces))
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
      await message.channel.send(ph.music_comment())

  if R.random() < 0.05:
    quote = ph.quote()
    if R.random() < 0.3: quote = ph.shuffle_text(quote)
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
      ph.blend_images(img1, img2)
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
    ph.edit(img)
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
  url, desc = ph.image(query, mime)

  embed = discord.Embed(title=query, description=desc, url=url)
  embed.set_image(url=url)

  log(f'{ctx.author.name} wants a picture of {query if query is not None else "..."}')
  await ctx.reply(embed=embed, mention_author=False)

@bot.command(name='quote', help='wisdom from the masters')
async def quote(ctx):
  await ctx.reply(ph.general_quote(proper=True), mention_author=False)

@bot.command(name='factabout', help='gives you a fact about something')
async def factabout(ctx, *, args): 
  await ctx.reply(ph.wiki_fact(args))

@bot.command(name='talkabout', help='get Phil\'s thoughts about something')
async def comment(ctx, *, topic):
  # search twitter for the given string
  comment = ph.twitter_search(topic) if len(topic) else ph.twitter_search()

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
    await ctx.reply(ph.compare(args[0], args[1]), mention_author=False)

@bot.command(name='define', help='learn the definition of a word or phrase')
async def define(ctx, *, query):
  if len(query) > 0:
    log(f'{ctx.author.name} has defined \'{query}\' for the channel')
    await ctx.reply(f'**{query}**: {ph.urban_definition(query)}', mention_author=False)

@bot.command(name='todo', help='get an item from the Post-Quarantine Bucket List')
async def todo(ctx):
  log(f'{ctx.author.name} needs something to do...')
  await ctx.reply(ph.get_todo(with_number=True), mention_author=False)

@bot.command(name='emojify', help='fill text with emojis')
async def emojify(ctx):
  msg = await ctx.history(limit=2).flatten()
  await ctx.send(f'{ph.emojify(msg[1].content)}')

@bot.command(name='clap', help='clap 👏 a 👏 message 👏')
async def clap(ctx):
  msg = await ctx.history(limit=2).flatten()
  txt = msg[1].content
  res = ''
  for w in txt.split(' '): res += f'{w} 👏 '
  await ctx.send(res)

if __name__ == '__main__':
  bot.run(DISCORD_TOKEN)
