from discord.ext import commands
import discord
import logging
import requests
from random import choice
from youtube_dl import YoutubeDL
from youtubesearchpython import VideosSearch

def url():
  res = VideosSearch('hours interrupted', limit=30).result()
  return choice([ x['link'] for x in res['result'] ]) 

YTDL_OPTS = { 
  'format': 'worstaudio', 
  'noplaylist': 'True', 
  'outtmpl': 'audio/shit.%(ext)s'
}
FFMPEG_OPTS = { 'options': '-vn' }
class Audio(commands.Cog, name='Audio'):
  def __init__(self, bot):
    self.bot = bot
    self.player = None

  @commands.command(name='join')
  async def join(self, ctx):

    if (v := ctx.message.author.voice):
      voice = await v.channel.connect()

      with YoutubeDL(YTDL_OPTS) as ydl:
        info = ydl.extract_info(url(), download=False)
        vid = info['formats'][0]['url']
        logging.info(vid)

      voice.play(discord.FFmpegPCMAudio(vid))
      
      while voice.is_playing():
        await asyncio.sleep(1)

      await voice.disconnect()


  @commands.command(name='leave')
  async def leave(self, ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_connected():
      await vc.disconnect()


def setup(bot):
  bot.add_cog(Audio(bot))
