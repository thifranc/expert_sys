#!/usr/bin/python3

import re

from parser import Parser

class Graph:

  def __init__(self):
    self.conclusions = []
    self.premisses = []
    self.graph = {}

  """parenthesis arent useful as conclusion can only contain + operator"""
  getConclusionFactPattern = re.compile('!?[a-z]', re.I)

  def handle_conclusion(self, conclusion):
    if Parser.negationInConclusionPattern.findall(conclusion):
      Parser.parse_error('add_rules-Negation')
    elif Parser.badPatternInConclusion.findall(conclusion):
      Parser.parse_error('add_rules-BadPattern')
    else:
      return Graph.getConclusionFactPattern.findall(conclusion)

  def append_conclusion(self, left_member, right_member, isDoubleEquivalence):
    conclusions = self.handle_conclusion(right_member)
    if isDoubleEquivalence:
      conclusions += self.handle_conclusion(left_member)
    #print('conclusions are ------> ',conclusions)
    if conclusions:
      for conclusion in conclusions:
        if not conclusion in self.graph:
          self.graph[conclusion] = []
        self.graph[conclusion].append(left_member)
