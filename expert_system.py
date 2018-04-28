#!/usr/bin/python3

import argparse
import os
import re
import collections
from parser import Parser
from resolver import Resolver

if __name__ == '__main__':

  ignored_line = re.compile('^(#|$)')
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help='File that contain queries and facts')
  args = parser.parse_args()

  parser = Parser()
  resolvers = []

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
      #print('facts to begin with -- ', parser.facts)
      #print('queries to solve -- ', parser.queries)
      #for key in sorted(parser.rules):
      #  print(parser.rules[key], ' => ', key)
      for query in parser.queries:
        resolvers.append(Resolver(parser.facts, parser.rules, query))
  except (NameError, PermissionError, IsADirectoryError) as error:
    print(error)
    exit(1)

# print(text_input)
