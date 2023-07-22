from discord.ext import commands
from discord import File
import requests
import regex
from utils import *

def error(icon=None, style=None, title=None, text=None, L=None, Lg=False, C=None, Cg=False, R=None, Rg=False):
  url = 'http://atom.smasher.org/error/xp.png.php?'

  if icon not in icons: icon = choice(icons)
  if style not in ['xp', '98']: style = choice(['xp', '98'])
  url += f'icon={icon}&style={style}'

  if title is not None: url += f'&title={title}'
  if text  is not None: url += f'&text={text}'

  if L is not None: url += f'&b1={L}' + ('&b1g=x' if Lg else '')
  if C is not None: url += f'&b2={C}' + ('&b2g=x' if Cg else '')
  if R is not None: url += f'&b3={R}' + ('&b3g=x' if Rg else '')

  url = url.replace(' ', '+')
  r = requests.get(url, stream=True)

  with open('img/error.png', 'wb') as f:
    r.raw.decode_content = True
    shutil.copyfileobj(r.raw, f)


class Error(commands.Cog, name='Error'):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='error')
  async def error(self, ctx, *arg):

    title = choice(todo().split(' '))
    text = todo()
    Lt = None
    Ct = None
    Rt = random_word()

    if len(arg) >= 1: title = arg[0]
    if len(arg) >= 2: text = arg[1]
    if len(arg) >= 3: Rt = arg[2]
    if len(arg) >= 4: Ct = arg[3]
    if len(arg) >= 5: Lt = arg[4]

    Lg = random() < 0.4
    Cg = random() < 0.4
    Rg = random() < 0.4

    error(title=title, text=text, L=Lt, Lg=Lg, C=Ct, Cg=Cg, R=Rt, Rg=Rg)

    f = File('./img/error.png')
    await ctx.send(file=f)

def setup(bot):
  bot.add_cog(Error(bot))

