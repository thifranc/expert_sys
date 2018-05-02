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
        line = re.sub('\s', '', line)
        line_is_ignored = ignored_line.match(line)
        if line_is_ignored is not None:
          continue
        parser.handle_line(line)
      resolver = Resolver(parser.facts, parser.rules)
      for query in parser.queries:
        response = resolver.resolve_query(query)
        print('query ', query, ' has resolved to : ', response)
  except (NameError, PermissionError, IsADirectoryError) as error:
    print(error)
    exit(1)
