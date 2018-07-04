#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import subprocess
import shutil

def exit():
  # Remove the tmp dir and exit gracefully
  shutil.rmtree('tmp')
  sys.exit(0)

def edit(svg_file, dir, name):
  # Copy the svg file to tmp/
  base_filename = svg_file[svg_file.index('/') + 1 : svg_file.rindex('.')]
  tmp_filename = 'tmp/{}_{}_tmp.svg'.format(base_filename, name)
  shutil.copyfile(svg_file, tmp_filename)
  
  # Open the temp svg file in Inkscape
  inkscape_tmp = subprocess.Popen(['inkscape', tmp_filename])
  
  # Wait for the user to edit it, make them type "done" to make sure they don't accidentally press enter
  done = None
  while done != 'done':
    done = input('Type "done" when done editing "{}.svg" as {}: '.format(base_filename, name)).lower()
  
  # Kill the Inkscape window
  inkscape_tmp.terminate()
  inkscape_tmp.kill()
  
  # Copy the temp file to the relevant directory
  new_filename = '{}/{}.svg'.format(dir, base_filename)
  shutil.copyfile(tmp_filename, new_filename)

def handle_file(svg_file):
  basename = svg_file[svg_file.index('/') + 1:]
  
  print()
  print('Image:', basename)
  
  # Open the original file in Inkscape
  inkscape_original = subprocess.Popen(['inkscape', svg_file])
  
  # Ask the user whether they want to edit to make a normal or just use the image
  while True:
    edit_normal = input('Edit normal? (y/n) ').lower()
    if edit_normal in ('y', 'n', 'exit', 'delete'):
      break
  
  if edit_normal == 'exit':
    exit()
  elif edit_normal == 'delete':
    os.remove(svg_file)
    return
  
  # Kill the original Inkscape "viewer" (not editing in this window)
  inkscape_original.terminate()
  inkscape_original.kill()
  
  if edit_normal == 'y':
    edit(svg_file, 'normals', 'normal')
  elif edit_normal == 'n':
    # just copy the file to normals/
    shutil.copyfile(svg_file, 'normals/' + basename)
  
  # Assume we always want to edit the variant
  print('Opening editor to edit variant...')
  edit(svg_file, 'variants', 'variant')
  
  # Remove the original file
  os.remove(svg_file)

# Make normals, variants, and tmp directories if they don't exist
try:
  os.mkdir('normals')
except FileExistsError:
  pass

try:
  os.mkdir('variants')
except FileExistsError:
  pass

try:
  os.mkdir('tmp')
except FileExistsError:
  pass

# Get the graphics filenames
svg_files = glob.glob('graphics/*.svg')
if not svg_files:
  print('No graphics found!')
  sys.exit(-1)

print('Use "exit" to exit at any point.')

for svg_file in svg_files:
  handle_file(svg_file.replace('\\', '/'))
