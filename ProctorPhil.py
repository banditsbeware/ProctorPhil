# ProctorPhil

import os
import re
import discord
import random as R
from discord.ext import tasks, commands

from yt import YTDL




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

import error as e
