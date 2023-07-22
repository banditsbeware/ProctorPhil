import os
import re
import sys
import requests
import random as R

import shutil
img_src_RE = re.compile('(?<=\sdata-src=").*?(?=")')
img_alt_RE = re.compile('(?<=\salt=").*?(?=")')
def image(query=None, mime=None):
  # build request URL
  url = 'https://commons.wikimedia.org/w/index.php?search='

  if query is None:
    url += random_word()
  else:
    url += query.replace(' ', '+')

  url += '&title=Special:MediaSearch&go=Go&type=image'

  # filter by file type (.png, .gif, etc)
  if mime is not None: url += f'&filemime={mime}'

  # entire results page HTML
  html = requests.get(url).text

  imgs = img_src_RE.findall(html)       # all image URLs  
  alts = img_alt_RE.findall(html)[:-4]  # associated alt text

  # no images found - try a random query
  if len(imgs) == 0: return image(mime=mime)

  img_number = R.randint(0, len(imgs)-1)

  aboutstr = alts[img_number]
  imageurl = imgs[img_number]

  return imageurl, aboutstr


from PIL import Image
def blend_images(path1, path2):
  img1 = Image.open(path1)
  img2 = Image.open(path2).resize(img1.size)
  img2.convert(img1.mode)

  destfn = './img/blend.png'
  Image.blend(img1, img2, 0.5).save(destfn)

from png import *
def edit(path):

  im = Image.open(path)

  for _ in range(15):
    R.choice(FUNCTIONS)(im)
  im.save('./img/edit.png')
  return False
