import os
import random as R
from PIL import Image, ImageDraw

# absolute path of folder with some pics
IMGPATH = 'A:/the_gallery/the_image_gallery/'

def rand_image():
  i = IMGPATH + R.choice(os.listdir(IMGPATH))
  if os.path.isfile(i): return Image.open(i)
  else: return rand_image()

def compress_and_save(image):
  fn = f'{image.filename}_compressed'
  image.save(f'{fn}.jpeg', 'JPEG', dpi=[500,500], quality=10)
  image = Image.open(f'{fn}.jpeg')
  image.save(f'{fn}.png', 'PNG')
  os.remove(f'{fn}.jpeg')
  return f'{fn}.png'

def blend(img1, img2, a=None):
  if a is None: a = R.random()

  n1 = img1.filename[len(IMGPATH):]
  n2 = img2.filename[len(IMGPATH):]

  img2.convert(img1.mode)
  img2 = img2.resize(img1.size)

  destfn = f'{n1}_{n2}_blend.png'
  Image.blend(img1, img2, a).save(destfn)
  return destfn

def roloc():
  return (R.randint(0,255), R.randint(0,255), R.randint(0,255), R.randint(0,255))

def rand_box(s):
  w,  h  = s
  x0, y0 = R.randint(0,w), R.randint(0,h)
  x1, y1 = x0 + R.randint(0, w - x0), y0 + R.randint(0, h - y0)
  return [x0, y0, x1, y1]

def a_line(i):
  draw = ImageDraw.Draw(i)
  if R.random() < 0.5:
    y = R.randint(0, i.height)
    draw.line((R.randint(0, i.width), y, R.randint(0, i.width), y), fill=roloc(), width=R.randint(1,5))
  else:
    x = R.randint(0, i.width)
    draw.line((x, R.randint(0, i.height), x, R.randint(0, i.height)), fill=roloc(), width=R.randint(1,5))

def rectangle(i):
  draw = ImageDraw.Draw(i)
  box = rand_box(i.size)
  draw.rectangle(box, fill=None if R.random() < 0.8 else roloc(), outline=roloc(), width=R.randint(1,10))

def ellipse(i, hollow=False):
  draw = ImageDraw.Draw(i)
  box = rand_box(i.size)
  draw.ellipse(box, fill=None if R.random() < 0.8 else roloc(), outline=roloc(), width=R.randint(1,10))

def flip_a_box(i):
  crop = tuple(rand_box(i.size))
  i.paste(i.crop(crop).rotate(180), box=crop)

def spin_part(i):
  crop = tuple(rand_box(i.size))
  turn = R.randint(0,360)
  region = i.crop(crop)
  rotate = region.rotate(turn, expand=True)
  mask = Image.new('L', region.size, 255).rotate(turn, expand=True)
  rotate.putalpha(mask)
  i.paste(rotate, mask=mask, box=(crop[0], crop[1], crop[0]+mask.width, crop[1]+mask.height))

def smear(i):
  d = R.randint(2,20)       # offset for each frame
  v = R.choice([-1, 0, 1])  # vertical direction
  h = R.choice([-1, 0, 1])  # horizontal direction

  c = tuple(rand_box(i.size))
  region = i.crop(c)

  for x in range(R.randint(1,20)):
    try: i.paste(region, box=(c[0] + x*d*h, c[1] + x*d*v, c[2] + x*d*h, c[3] + x*d*v))
    except SystemError: break # raised when trying to paste outside image area

FUNCTIONS = [
  a_line,
  rectangle,
  ellipse,
  flip_a_box,
  spin_part,
  smear
]

def gif(i, N, dest):
  frames = [i.copy()]
  for f in range(N):
    R.choice(FUNCTIONS)(i)
    frames.append(i.copy())
  frames[0].save(dest, save_all=True, append_images=frames[1:], optimize=False, duration=1, loop=0)
