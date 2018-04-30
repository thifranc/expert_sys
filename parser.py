#!/usr/bin/python3

import os
import re

from token import Token
from error import Error

class Parser:

  implicationPattern = re.compile('^(.*?)(<?)=>(.*?)(#|$)')
  # re.I indicates that the regex will be csae-insensitive
  negationPattern = re.compile('![^a-z]', re.I)
  badPatternInConclusion = re.compile('[^)+(!a-z]', re.I)
  getFactsOrQueryPattern = re.compile('^[?=]((!?[a-z])*)(#|$)', re.I)
  tokenPattern = re.compile('^([a-z()+|^]|![a-z])+$', re.I)
  tokenPatternBis = re.compile('!?.', re.I)
  """parenthesis arent useful as conclusion can only contain + operator"""
  getConclusionFactPattern = re.compile('!?[a-z]', re.I)

  rules = {}

  @classmethod
  def handle_conclusion(self, conclusion):
    if Parser.negationPattern.findall(conclusion):
      Error('add_rules', '-Negation')
    elif Parser.badPatternInConclusion.findall(conclusion):
      Error('add_rules', '-BadPattern')
    else:
      return Parser.getConclusionFactPattern.findall(conclusion)

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
      Error('testParenthesisSyntax')

  @classmethod
  def parse_string_to_token(cls, string):
    """
      ex: parse_string_to_token('(!a + B) | c')
      => [ '(', '!a', '+', 'B', ')', '|', 'c' ]
    """
    if not Parser.tokenPattern.match(string):
      Error('parse_string_to_token', '-bad pattern in token')
      return
    tokens = Parser.tokenPatternBis.findall(string)
    tokenInstances = []
    lastToken = None
    for token in tokens:
      curToken = Token(token)
      if lastToken and Token.token_are_the_same_type(lastToken, curToken):
        print('compare - ', lastToken.token, curToken.token)
        Error('parse_string_to_token', '-repetition not good')
        return
      tokenInstances.append(curToken)
      lastToken = tokenInstances[-1]
    return tokenInstances

  def __init__(self):
    self.facts = []
    self.queries = []

  def append_conclusion(self, left_member, right_member, isDoubleEquivalence):
    conclusions = Parser.handle_conclusion(right_member)
    if isDoubleEquivalence:
      self.append_conclusion(right_member, left_member, None)
    if conclusions:
      for conclusion in conclusions:
        if not conclusion in self.rules:
          self.rules[conclusion] = []
        self.rules[conclusion].append(left_member)

  def add_rules(self, line):
    matches = Parser.implicationPattern.match(line)
    if matches is None:
      Error('add_rules')
    else:
      #print(
      #    'line >>> ',
      #    matches.group(1), matches.group(2), '=>',matches.group(3)
      #    )
      self.append_conclusion(matches.group(1), matches.group(3), matches.group(2))

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
      Error('set_facts')
    facts = self.parse_facts_or_queries(line)
    #print('facts are --- ', facts)
    self.facts = facts

  def set_query(self, line):
    if self.queries:
      Error('set_query')
    queries = self.parse_facts_or_queries(line)
    #print('queries are --- ', queries)
    self.queries = queries

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
