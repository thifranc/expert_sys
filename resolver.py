#!/usr/bin/python3

from nodes import Node
from token import Token

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

  def or_operation(self, left, right):
    if left or right:
      return True
    else:
      return None

  def xor_operation(self, left, right):
    if (left and not right) or (not left and right):
      return True
    else:
      return None

  def and_operation(self, left, right):
    if left and right:
      return True
    else:
      return None

  def error():
    print('ERROR CUT ALL SHIT')

  def resolve_premisse_value(self, premisse, parents):
    if Token.is_token(premisse):
      if parents and premisse in parents:
        return None
      return self.resolve_node(premisse, parents + [premisse])
    else:
      return self.resolve_premisse(premisse, parents + [premisse])

  def resolve_premisse(self, premisse, parents):
    #parent tracking to prevent infinite loop here
    operators = list(premisse.keys())

    left_member = premisse[operators[0]][0]
    right_member = premisse[operators[0]][1]

    left_member_value = self.resolve_premisse_value(left_member, parents)
    right_member_value = self.resolve_premisse_value(right_member, parents)

    premisse_value = {
      '|': self.or_operation,
      '+': self.and_operation,
      '^': self.xor_operation
    }.get(operators[0], self.error)(left_member_value, right_member_value)
    return premisse_value

  def resolve_node_value(self, node, parents):
    if node._name in self._facts:
      return True
    value = None
    for premisse in node._premisses:
      if self.resolve_premisse_value(premisse, parents):
        value = True
        break
    return value

  def resolve_node(self, name, parents):
    if name in self._nodes:
      return self._nodes[name]._value
    else:
      node = Node(name, self._rules[name] if name in self._rules else [])
      value = self.resolve_node_value(node, parents)
      node._value = value
      self.add_node(node)
      return value

  def resolve_query(self, query):
    anti_query = ''
    if query[0] == '!':
      anti_query = query[1:]
    else:
      anti_query = '!' + query
    node_value = self.resolve_node(query, [])
    anti_node_value = self.resolve_node(anti_query, [])
    if node_value == None and anti_node_value == None:
      return 'unknown'
    elif node_value == None and anti_node_value == True:
      return 'false'
    elif node_value == True and anti_node_value == None:
      return 'true'
    else:
      return 'contradiction'
