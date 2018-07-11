#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A script to process the SVGs in normals/ and variants/ into 512x512 PNG files. Note that Inkscape must be installed
and on the PATH for this script to run.
"""


import sys
import os
import glob
import subprocess
import urllib


def process(img):
  # svg -> png conversion is delegated to Inkscape
  # Please don't name the things anything like "&& rm -rf / #.svg", that would make me very sad
  png = img[:-4] + '.png'
  print('Converting {}...'.format(img))
  try:
    subprocess.run(['inkscape', img, '-e', png, '--export-width=512', '--export-height=512'],
                   check=True)
  except subprocess.CalledProcessError as e:
    print('Inkscape (called with command {}) failed to convert {} to PNG with error code {}'
          .format(e.cmd, img, e.returncode))


def get_images_from_dir(dir, ext, exit_if_none=True):
  images = glob.glob('{}/*.{}'.format(dir, ext))
  
  if exit_if_none and not images:
    print('No {} images found in directory {}/!'.format(ext.upper(), dir))
    sys.exit(-1)
  
  return [img.replace('\\', '/') for img in images]


def get_images():
  # Images which exist in both directories and don't already have a PNG with the same name
  normal_svg = get_images_from_dir('normals', 'svg')
  variant_svg = get_images_from_dir('variants', 'svg')
  normal_png = get_images_from_dir('normals', 'png', exit_if_none=False)
  variant_png = get_images_from_dir('normals', 'png', exit_if_none=False)
  
  return [base + '.svg' for base in map(lambda svg: os.path.splitext(os.path.basename(svg))[0], normal_svg)
          if 'variants/{}.svg'.format(base) in variant_svg and 'normals/{}.png'.format(base) not in normal_png
          and 'variants/{}.png'.format(base) not in variant_png]


def main():
  # Make sure both directories exist
  if not os.path.isdir('normals') or not os.path.isdir('variants'):
    print('normals/ or variants/ directory did not exist!')
    sys.exit(-1)
  
  # Process the list of images
  for svg in get_images():
    for dir in 'normals/', 'variants/':
      img = dir + svg
      
      try:
        process(img)
      except Exception as e:
        print('Failed to process {}: {}'.format(img, e))


if __name__ == '__main__':
  main()
