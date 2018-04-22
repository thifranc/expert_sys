#!/usr/bin/python3

import os
import re

class Parser:

  implicationPattern = re.compile('^(.*?)(<?)=>(.*?)(#|$)')
  # re.I indicates that the regex will be csae-insensitive
  negationPattern = re.compile('![^a-z]', re.I)
  badPatternInConclusion = re.compile('[^)+(!a-z]', re.I)
  getFactsOrQueryPattern = re.compile('^[?=]((!?[a-z])*)(#|$)', re.I)
  tokenPattern = re.compile('[a-z()+|^]|![a-z]', re.I)

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

  @classmethod
  def parse_string_to_token(cls, string):
    """
      ex: parse_string_to_token('(!a + B) | c')
      => [ '(', '!a', '+', 'B', ')', '|', 'c' ]
    """
    #those two lines should be removed as they're useless
    matches = Parser.tokenPattern.findall(string)
    print('matches -- ', matches)
    return Parser.tokenPattern.findall(string)

  def __init__(self):
    self.facts = []
    self.query = []
    self.premisses = []

  def add_rules(self, line):
    from graph import Graph
    if not self.graph:
      self.graph = Graph()
    matches = Parser.implicationPattern.match(line)
    """ line == end is to be removed """
    if line == 'end':
      print(self.graph.graph)
    if matches is None:
      Parser.parse_error('add_rules')
    else:
      #print(
      #    'line >>> ',
      #    matches.group(1), matches.group(2), '=>',matches.group(3)
      #    )
      self.graph.append_conclusion(matches.group(1), matches.group(3), matches.group(2))

  def parse_facts_or_queries(self, line):
    matchedItems = list(Parser.getFactsOrQueryPattern.match(line).group(1))
    listMatchedItems = []
    addNegation = None
    for matchedItem in matchedItems:
      if matchedItem == '!':
        addNegation = True
        continue
      else:
        listMatchedItems.append('!'+matchedItem if addNegation else matchedItem)
        addNegation = None
    return listMatchedItems

  def set_facts(self, line):
    if self.facts:
      Parser.parse_error('set_facts')
    facts = self.parse_facts_or_queries(line)
    #print('facts are --- ', facts)
    self.facts = facts

  def set_query(self, line):
    if self.query:
      Parser.parse_error('set_query')
    queries = self.parse_facts_or_queries(line)
    #print('queries are --- ', queries)
    self.query = queries

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
