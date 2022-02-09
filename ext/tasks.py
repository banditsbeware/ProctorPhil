from discord import Game
from discord.ext import tasks, commands
import logging
import requests
from random import choice

# for recurring tasks
class Tasks(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    with open('./vocab/faces.txt', 'r') as f: txt = f.read()
    self.faces = txt.split('\n')

  @tasks.loop(minutes=30)
  async def update_presence(self):
    status = requests.get('https://pigeon.dog/todo').text
    if len(status) > 128: status = status[:125] + '...'
    await self.bot.change_presence(activity=Game(name=status))
    logging.info(f'playing {status}')

  @tasks.loop(minutes=23)
  async def update_vc_face(self):
    g = self.bot.guilds[0]
    c = g.get_channel(806679944305311768)
    await c.edit(name=choice(self.faces))

  @commands.Cog.listener()
  async def on_ready(self):
    await self.bot.wait_until_ready()
    self.update_presence.start()
    self.update_vc_face.start()


def setup(bot):
  bot.add_cog(Tasks(bot))