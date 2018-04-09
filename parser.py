import os
import re

class Parser:
  """test"""
  implicationPattern = re.compile('^(.*?)(<?)=>(.*?)(#|$)')

  def __init__(self):
    """caca"""
    self.facts = []
    self.query = []
    self.premisses = []

  def add_rules(self, line):
    matches = Parser.implicationPattern.match(line)
    print(matches.group(1))
    print(matches.group(2))
    print(matches.group(3))
    return()

  def set_facts(self, line):
    if self.facts:
      self.parse_error()
    self.facts.append(line)

  def set_query(self, line):
    if self.query:
      self.parse_error()
    self.query.append(line)

  def parse_error(self):
    print('parse error')
    exit(1)

  def handle_line(self, line):
    array = {
      '?': self.set_query,
      '=': self.set_facts
    }.get(line[0], self.add_rules)(line)

if __name__ == '__main__':
  parser = Parser()
  expectation = 5
  if 4 is not 5:
    print('error')
  print('bring me some tests')
