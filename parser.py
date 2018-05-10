#!/usr/bin/python3

import os
import re

from tokens import Token
from parse_error import ParseError
from termcolor import colored

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

  @classmethod
  def handle_conclusion(self, conclusion):
    if Parser.negationPattern.findall(conclusion):
      raise ParseError('negation found in conclusion')
    elif Parser.badPatternInConclusion.findall(conclusion):
      raise ParseError('wrong pattern found in conclusion')
    else:
      return Parser.getConclusionFactPattern.findall(conclusion)

  @classmethod
  def parse_string_to_token(cls, string):
    """
      ex: parse_string_to_token('(!a + B) | c')
      => [ '(', '!a', '+', 'B', ')', '|', 'c' ]
    """
    if not Parser.tokenPattern.match(string):
      raise ParseError('bad token pattern')
    tokens = Parser.tokenPatternBis.findall(string)
    tokenInstances = []
    lastToken = None
    for token in tokens:
      curToken = Token(token)
      tokenInstances.append(curToken)
      if not curToken.is_parenthesis() and Token.token_are_the_same_type(lastToken, curToken):
        raise ParseError('token repetition detected')
      if not curToken.is_parenthesis():
        lastToken = tokenInstances[-1]
    return tokenInstances

  def __init__(self):
    self.facts = []
    self.queries = []
    self.rules = {}

  def __str__(self):
    return("Facts are : {}\n\nRules are :\n{}\nWhat we want to know : {}\n".format(
      self.facts,
      self.print_rules(),
      self.queries
    ))

  def print_rules(self):
    ret = ""
    for rule in self.rules:
      ret += '\t{} can be resolved with : \n'.format(colored(rule, 'yellow'))
      for premisse in self.rules[rule]:
        ret += '\t   {}\n'.format(colored(premisse, 'yellow'))
    return ret


  def append_conclusion(self, left_member, right_member, isDoubleEquivalence):
    if not right_member:
      raise ParseError('No right member')
    if not left_member:
      raise ParseError('No left member')
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
      raise ParseError('No implication symbol found on line')
    else:
      self.append_conclusion(matches.group(1), matches.group(3), matches.group(2))

  def parse_facts_or_queries(self, line):
    regexResult = Parser.getFactsOrQueryPattern.match(line)
    if not regexResult and len(line) > 0:
      raise ParseError('Bad pattern ')
    matchedItems = list(regexResult.group(1))
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
      raise ParseError('file not well formatted, facts given twice')
    facts = self.parse_facts_or_queries(line)
    self.facts = facts

  def set_query(self, line):
    if self.queries:
      raise ParseError('file not well formatted, queries given twice')
    queries = self.parse_facts_or_queries(line)
    self.queries = queries

  def handle_line(self, line):
    array = {
      '?': self.set_query,
      '=': self.set_facts
    }.get(line[0], self.add_rules)(line)
