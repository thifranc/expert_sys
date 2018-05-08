#!/usr/bin/python3

import argparse
import os
import re
import collections
from parser import Parser
from resolver import Resolver
from parse_error import ParseError
from contradiction_error import ContradictionError

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
          try:
            parser.handle_line(line)
          except ParseError as exception:
            print('caca')
            print('Parse error of type : {} detected on line\n\t=>{}'.format(exception.exception_type, line))
            exit(1)

    resolver = Resolver(parser.facts, parser.rules)
    for query in parser.queries:
      try:
        response = resolver.resolve_query(query)
        print('query ', query, ' has resolved to : ', response)
      except ContradictionError as exception:
        print('Contradiction detected on {0} that is {1} while his opposite is also {1}'.format(exception.name, exception.value))
  except (NameError, PermissionError, IsADirectoryError) as error:
    print(error)
    exit(1)
