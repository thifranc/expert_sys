import os
import re

class Parser:
  """test"""
  implicationPattern = re.compile('^(.*?)(<?)=>(.*?)(#|$)')

  negationInConclusionPattern = re.compile('![^a-z]', re.I)

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
    """caca"""
    self.facts = []
    self.query = []
    self.premisses = []

  def add_rules(self, line):
    matches = Parser.implicationPattern.match(line)
    premisse = matches.group(1)
    conclusion = matches.group(3)
    print('premisse : ', premisse)
    Parser.testParenthesisSyntax(premisse)
    print('conclucion : ', conclusion)
    Parser.testParenthesisSyntax(conclusion)
    if Parser.negationInConclusionPattern.match(conclusion) is not None:
      Parser.parse_error('add_rules')
    # matches.group(1))
    # print(matches.group(2))
    # print(matches.group(3))
    return()

  def set_facts(self, line):
    if self.facts:
      Parser.parse_error()
    self.facts.append(line)

  def set_query(self, line):
    if self.query:
      Parser.parse_error()
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
