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
from termcolor import colored

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
            print(colored('Parse error of type : {} detected on line\n\t --> {}'.format(exception.exception_type, line), 'red'))
            raise FileError()

    if not parser.queries:
      print(colored('No queries furnished', 'red'))
      raise FileError
    if args.verbose:
      print(parser)
    resolver = Resolver(parser.facts, parser.rules, args.verbose)
    for query in parser.queries:
      try:
        if args.verbose:
          print(colored('Query to solve : {}'.format(query), 'yellow'))
        response = resolver.resolve_query(query)
        print(colored('query {}  has been resolved to : {}'.format(query, response), 'green'))
      except ContradictionError as exception:
        print(colored('Contradiction detected on {0} that is {1} while his opposite is also {1}'.format(exception.name, exception.value), 'red'))
  except (FileNotFoundError, NameError, PermissionError, IsADirectoryError, UnicodeDecodeError) as error:
    print(colored(error, 'red'))
    raise FileError()

if __name__ == '__main__':
  ignored_line = re.compile('^(#|$)')
  parser = argparse.ArgumentParser()
  parser.add_argument("file", nargs="?", help='File that contain queries and facts')
  parser.add_argument("-m", "--multiple", nargs="+", help='add_multiple files at one time')
  parser.add_argument("-d", "--directory", help='add_multiple files at one time')
  parser.add_argument("-v", "--verbose", action='store_true', help='add clarity to output')
  args = parser.parse_args()

  files = [args.file]

  if args.multiple:
    files.extend(args.multiple)

  # append all files from directory given as argument
  if args.directory:
    try:
      files.extend([os.path.join(args.directory, f) for f in os.listdir(args.directory) if os.path.isfile(os.path.join(args.directory, f))])
    except NotADirectoryError:
      print(colored('[Errno FuckYou] {} is not a directory\n'.format(args.directory), 'red'))

  for filename in filter(None, files):
    try:
      print(colored("Resolving file : {}".format(filename), 'cyan'))
      resolve_file(filename)
    except FileError:
      pass
    finally:
      print(colored('\n<-------->\n', 'cyan'))


