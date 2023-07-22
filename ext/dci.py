from discord.ext import commands
from discord import File
import requests
import regex

def schedule():
    pass

class DCI(commands.Cog, name='DCI'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='schedule')
  async def schedule(self, ctx, *arg):

    await ctx.send("schedule")

def setup(bot):
  bot.add_cog(DCI(bot))


if __name__ == '__main__':
    print( schedule() )
