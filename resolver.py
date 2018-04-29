#!/usr/bin/python3

from nodes import Node

class Resolver:

  _nodes = {}
  _rules = {}
  _facts = []

  def __init__(self, facts, rules):
    for fact in facts:
      node = Node(fact, [])
      node._value = True
      self.add_node(node)
    self._rules = rules
    self._facts = facts

  def add_node(self, node):
    self._nodes[node._name] = node

  def or_operation(self, premisse):
    print('or ope -- ', premisse)

  def xor_operation(self, premisse):
    print('xor ope -- ', premisse)

  def and_operation(self, premisse):
    print('and ope -- ', premisse)

  def error():
    print('ERROR CUT ALL SHIT')

  def resolve_premisse(self, premisse):
    #parent tracking to prevent infinite loop here
    operators = list(premisse.keys())
    array = {
      '|': self.or_operation,
      '+': self.and_operation,
      '^': self.xor_operation
    }.get(operators[0], self.error)(premisse[operators[0]])

  def resolve_node_value(self, node):
    if node._name in self._facts:
      return True
    value = None
    for premisse in node._premisses:
      if self.resolve_premisse(premisse):
        value = True
    return value

  def resolve_node(self, name):
    if self._nodes[name]:
      return self._nodes[name]._value
    else:
      node = Node(name, self._rules[name] if self._rules[name] else [])
      value = self.resolve_node_value(node)
      node._value = value
      self.add_node(node)

  def resolve_query(self, query):
    anti_query = '!' + query if query[0] == '!' else query[1:]
    self.resolve_node(query)
    self.resolve_node(anti_query)
    node_value = self._nodes[query]._value
    anti_node_value = self._nodes[anti_query]._value
    if node_value == None and anti_node_value == None:
      return 'unknown'
    elif node_value == None and anti_node_value == True:
      return 'false'
    elif node_value == True and anti_node_value == None:
      return 'true'
    else:
      return 'contradiction'
