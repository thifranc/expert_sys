#!/usr/bin/python3

import argparse
import os
import re
import collections
from parser import Parser
from resolver import Resolver
from parse_error import ParseError
from contradiction_error import ContradictionError
from file_error import FileError

def resolve_file(filename):
  parser = Parser()
  try:
    with open(filename, 'r') as file:
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
            raise FileError()

    resolver = Resolver(parser.facts, parser.rules)
    for query in parser.queries:
      try:
        response = resolver.resolve_query(query)
        print('query ', query, ' has resolved to : ', response)
      except ContradictionError as exception:
        print('Contradiction detected on {0} that is {1} while his opposite is also {1}'.format(exception.name, exception.value))
  except (FileNotFoundError, NameError, PermissionError, IsADirectoryError) as error:
    print(error)
    raise FileError()

if __name__ == '__main__':
  ignored_line = re.compile('^(#|$)')
  parser = argparse.ArgumentParser()
  parser.add_argument("file", nargs="?", help='File that contain queries and facts')
  parser.add_argument("-m", "--multiple", nargs="+", help='add_multiple files at one time')
  args = parser.parse_args()

  files = [args.file]
  files.extend(args.multiple)
  for filename in filter(None, files):
    try:
      print("Resolving file : ", filename)
      resolve_file(filename)
    except FileError:
      pass
    finally:
      print('\n<-------->\n')


