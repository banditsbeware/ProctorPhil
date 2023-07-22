from discord.ext import commands
import regex as re
import requests
import json
import urbanpython
from twython import Twython
from random import choice
from utils import *

with open('./config.json', 'r') as f:
  config = json.load(f)


urban = urbanpython.Urban(config['urban_dictionary_key'])
def urban_definition(query):
  result = urban.search(query)
  defn = f'{result.definition}\n\n{result.example}'
  defn = re.sub(r'(\[|\]|\{|\})', '', defn)
  return defn


def wiki_fact(subject):
  t = requests.get('http://en.wikipedia.org/wiki/Special:Random').text
  t = clean_tags(t)
  m = re.findall(r"\swas\s.*?\.|\sis\s.*?\.", t)
  if len(m) <= 2: return wiki_fact(subject)
  m = m[:-2]
  return f'{subject}{choice(m)}'


twitter = Twython(config['TW_APP_KEY'],   config['TW_APP_SEC'],
                  config['TW_OAUTH_KEY'], config['TW_OAUTH_SEC'])
def twitter_search(query=None):
  if query is None: query = random_word()

  # make request to twitter
  query += ' -filter:retweets -filter:replies'
  tweets = twitter.search(q=query, tweet_mode='extended', lang='en')['statuses']

  # if no tweets are found, search for a random word instead
  if len(tweets) == 0: return twitter_search()

  # choose a random result and clean text
  text = choice(tweets)['full_text']
  text = re.sub(' ??https?://.*/\w+ ??', '', text)
  text = re.sub('&amp;', '&', text)

  return text 


class Academia(commands.Cog, name="Academia"):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='define')
  async def define(self, ctx, *, query):
    with ctx.typing():
      await ctx.send(f'**{query}**: {urban_definition(query)}')

  @commands.command(name='factabout')
  async def factabout(self, ctx, *, args): 
    with ctx.typing():
      await ctx.send(wiki_fact(args))

  @commands.command(name='talkabout')
  async def talkabout(self, ctx, *, topic):
    with ctx.typing():
      comment = twitter_search(topic) if len(topic) else twitter_search()
      await ctx.send(comment)

  @commands.command(name='todo')
  async def todo(self, ctx):
    with ctx.typing():
      await ctx.send(todo())


def setup(bot):
  bot.add_cog(Academia(bot))
