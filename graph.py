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

  @classmethod
  def handle_conclusion(cls, conclusion):
    if Parser.negationInConclusionPattern.findall(conclusion):
      Parser.parse_error('add_rules-Negation')
    elif Parser.badPatternInConclusion.findall(conclusion):
      Parser.parse_error('add_rules-BadPattern')
    else:
      return Graph.getConclusionFactPattern.findall(conclusion)

  def get_conclusions(self, conclusion, premisse, isDoubleEquivalence):
    conclusions = Graph.handle_conclusion(conclusion)
    if isDoubleEquivalence:
      conclusions += Graph.handle_conclusion(premisse)
    print('conclusions are ------> ',conclusions)
    if conclusions:
      for conc in conclusions:
        if not conc in self.graph:
          self.graph[conc] = []
        self.graph[conc].append(premisse)
