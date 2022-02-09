from discord.ext import commands
import discord
import requests
from random import choice
from youtube_dl import YoutubeDL

# collection of videos of type "N hours of silence broken only by X"
v = [ 'hOwiw6RKkZ8', 'ameTtKHP5SA', '0Jzx25X80oA', 'QGroZXx2eGM', 'z6BSnp534L4', 'jvMCitR0-l4', 'MLw2vJPv5bc', 's6V4BjURhOs', 'H_slL1opzFc', 'bmDdHk_X864']
def url():
  return f'https://www.youtube.com/watch?v={choice(v)}'

YTDL_OPTS = { 
  'format': 'worstaudio', 
  'noplaylist': 'True', 
  'outtmpl': 'audio/shit.%(ext)s'
}
FFMPEG_OPTS = { 'options': '-vn' }

ytdl = YoutubeDL(YTDL_OPTS)

class YTDLSource(discord.PCMVolumeTransformer):
  def __init__(self, source, *, data, volume=0.5):
    super().__init__(source, volume)
    self.data = data
    self.title = data.get('title')
    self.url = data.get('url')

  @classmethod
  async def from_url(cls, url, *, loop=None, stream=False):

    loop = loop or asyncio.get_event_loop()

    data = await loop.run_in_executor(None, 
      lambda: ytdl.extract_info(url, download=not stream))

    if 'entries' in data:
      data = choice(data['entries'])

    filename = data['url'] if stream else ytdl.prepare_filename(data)
    return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTS), data=data)


class Audio(commands.Cog, name='Audio'):
  def __init__(self, bot):
    self.bot = bot
    self.player = None

  @commands.command(name='join')
  async def join(self, ctx):

    if ctx.message.author.voice:
      await ctx.message.author.voice.channel.connect()

      self.player = await YTDLSource.from_url(url(), loop=self.bot.loop, stream=True)

      ctx.voice_client.play(self.player,
        after=lambda e: logging.info(e) if e else None)


  @commands.command(name='leave')
  async def leave(self, ctx):
    vc = ctx.message.guild.voice_client
    if vc.is_connected():
      await vc.disconnect()


def setup(bot):
  bot.add_cog(Audio(bot))