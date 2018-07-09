#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A script to get images from openclipart.org"""


import urllib.request
import requests
import io
import json
import os
import re
import shutil
import subprocess
from PIL import Image


IMGS_PER_TIME = 10
SORT_BY = 'downloads' # probably best images first? who cares if they change?


current_page = -1


def get(position):
  global imgs, current_page
  page, position_on_page = divmod(position, IMGS_PER_TIME)
  
  if page != current_page:
    url = 'https://openclipart.org/search/json/?page={}&sort={}&amount={}'.format(page + 1, SORT_BY, IMGS_PER_TIME)
    with urllib.request.urlopen(url) as res:
      res_body = res.read()
      imgs = json.loads(res_body.decode('utf-8'))
      current_page = page
  
  return imgs['payload'][position_on_page]


def main():
  # Try to load the last position from openclipart_position.txt
  try:
    with open('openclipart_position.txt', 'r') as pos_file:
      position = int(pos_file.read().strip())
  except (IOError, ValueError):
    position = 0

  # Make the tmp folder
  try:
    os.mkdir('tmp')
  except FileExistsError:
    # it already exists, that's fine
    pass

  # Make the graphics folder
  try:
    os.mkdir('graphics')
  except FileExistsError:
    # it already exists, that's fine
    pass

  while True:
    img_json = get(position)
    
    # Show the image to the user
    img_response = requests.get(img_json['svg']['png_full_lossy'])
    img_file = io.BytesIO(img_response.content)
    img = Image.open(img_file).convert('RGBA')
    
    new_img = Image.new('RGBA', img.size, (255, 255, 255, 255))
    new_img.paste(img, mask=img)
    temp_filename = 'tmp\\{}.png'.format(position)
    new_img.save(temp_filename)
    
    viewer = subprocess.Popen(['mspaint', temp_filename])
    
    # Let them choose whether to keep it or not
    while True:
      proceed = input('Use "{}" (y/n)? '.format(img_json['title'])).lower()
      if proceed in ('y', 'n', 'exit'):
        break
    
    # Clean up the image viewer
    viewer.terminate()
    viewer.kill()
    
    if proceed == 'exit':
      break
    
    if proceed == 'y':
      # Save the svg file
      safe_title = re.sub(r'[\W]', '', re.sub(r'\s+', '_', img_json['title'])).lower()
      filename = 'graphics/openclipart_{}_{}.svg'.format(position, safe_title)
      urllib.request.urlretrieve(img_json['svg']['url'], filename)
    
    position += 1

  # Delete the tmp folder
  shutil.rmtree('tmp')

  # Save position to openclipart_position.txt
  with open('openclipart_position.txt', 'w') as pos_file:
    pos_file.write(str(position))


if __name__ == '__main__':
  main()
