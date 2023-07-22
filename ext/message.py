from discord.ext import commands
from random import random, choice, shuffle
import regex as re
import requests

genre_url = 'https://binaryjazz.us/wp-json/genrenator/v1/genre/'
genre_comments = [
  'That sounds like _.', 'That\'s some good _.', 'banger', 'this slaps', 'this smacks',
  'I can\'t tell if that\'s _ or _.', 'This is the intersection of _ and _.',
  'This redefines _.', 'I love _.', 'Thank you for sharing some classic _.', 
  '_-type beat', '_ vibes']
def music_comment():
  comment = choice(genre_comments)
  while comment.find('_') >= 0:
    comment = comment.replace('_', requests.get(genre_url).text, 1)
  comment = comment.replace('"', '*')
  comment = comment.replace('\\', '')
  return comment

h2 = re.compile(r'(?<=<h2>)[\s\S]*?(?=<h2>)')
dd = re.compile(r'(?<=<dd>)[\s\S]*?(?=</dd>)|(?<=<ul><li>)[\s\S]*?(?=</li>|<ul>)')
def general_quote():
  text = requests.get('https://en.wikiquote.org/wiki/Special:Random').text
  text = ''.join(h2.findall(text)[:-1])
  text = clean_tags(choice(dd.findall(text)))
  return text

def kanye_quote():
  return requests.get('https://api.kanye.rest?format=text').json()['quote']

def anime_quote():
  return requests.get('https://animechan.vercel.app/api/random').json()['quote']

def quote():
  return choice([ general_quote, kanye_quote, anime_quote ])()

def shuffle_text(string):
  words = string.split(' ')
  shuffle(words)
  return ' '.join(words)

emlist = ['😀', '😖', '👏', '🍆💦', '😬', '😔', '😞', '🙌', '💪', 
'🙏', '👀', '🗣', '👌', '😭', '😉', '😋', '🙇', '💫', '🔥', '✨', 
'™️', '🌈', '📈', '❤', '🅱', '💯', '💭', '😷', '😓', '😳', 
'😍', '™️', '♿️', '❌']
def emojify(text):
  text = text.split(' ')
  res = ''
  for word in text:
    if random() < 0.5: 
      res += choice(emlist)
      if random() < 0.5: 
        res += choice(emlist)
        if random() < 0.5: 
          res += choice(emlist)
    res += word + ' '
  return res

class Message(commands.Cog, name='Message'):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot: return

    msg = message.content

    # judge people's music suggestions in the music channel
    if message.channel.id == 817974358060040222:
      if re.search('://(open.spotify.com|youtu.be|www.youtube.com)/', msg) is not None:
        await message.channel.send(music_comment())

    # spontaneous utterances
    if random() < 0.01:
      Q = quote()
      if random() < 0.2: Q = shuffle_text(Q)
      await message.channel.send(Q)

  @commands.command(name='clap')
  async def clap(self, ctx):
    msg = await ctx.history(limit=2).flatten()
    txt = msg[1].content
    clapt = ' 👏 '.join( txt.split() )
    await ctx.send(clapt)

  @commands.command(name='emojify')
  async def emojify(self, ctx):
    msg = await ctx.history(limit=2).flatten()
    await ctx.send(f'{emojify(msg[1].content)}')

  @commands.command(name='quote')
  async def quote(self, ctx):
    await ctx.send(quote())


def setup(bot):
  bot.add_cog(Message(bot))
