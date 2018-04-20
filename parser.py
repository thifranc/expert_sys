#!/usr/bin/python3

import os
import re

class Parser:

  implicationPattern = re.compile('^(.*?)(<?)=>(.*?)(#|$)')
  negationInConclusionPattern = re.compile('![^a-z]', re.I)
  badPatternInConclusion = re.compile('[^)+(!a-z]', re.I)

  graph = None

  @classmethod
  def testParenthesisSyntax(cls, line):
    i = 0
    for char in line:
      if char == '(':
        i += 1
      elif char == ')':
        i -= 1
      if i < 0:
        break
    if i != 0:
      Parser.parse_error('testParenthesisSyntax')

  @classmethod
  def parse_error(cls, origin = ''):
    print('parse error from: ', origin)
    # exit(1)

  def __init__(self):
    self.facts = []
    self.query = []
    self.premisses = []

  def add_rules(self, line):
    from graph import Graph
    if not self.graph:
      self.graph = Graph()
    matches = Parser.implicationPattern.match(line)
    if line == 'end':
      print(self.graph.graph)
    if matches is None:
      Parser.parse_error('add_rules')
    else:
      print(
          'line >>> ',
          matches.group(1), matches.group(2), '=>',matches.group(3)
          )
      self.graph.get_conclusions(matches.group(3), matches.group(1), matches.group(2))

  def set_facts(self, line):
    if self.facts:
      Parser.parse_error('set_facts')
    self.facts.append(line)

  def set_query(self, line):
    if self.query:
      Parser.parse_error('set_query')
    self.query.append(line)

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
