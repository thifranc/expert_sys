#!/usr/bin/python3

import argparse
import os
import re
from parser import Parser

if __name__ == '__main__':

  ignored_line = re.compile('^(#|$)')
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help='File that contain queries and facts')
  args = parser.parse_args()

  parser = Parser()

  try:
    with open(args.file, 'r') as file:
      for line in file:
        # print(line)
        line = re.sub('\s', '', line)
        line_is_ignored = ignored_line.match(line)
        if line_is_ignored is not None:
          continue
        # print(line)
        parser.handle_line(line)
      # text_input = file.read()
  except (NameError, PermissionError, IsADirectoryError) as error:
    print(error)
    exit(1)

# print(text_input)
