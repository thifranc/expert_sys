#!/usr/bin/python3

from node import Node
from tokens import Token
from error import Error

class Resolver:
  """
  this class is used to resolve queries
  it holds a nodes attribute that contains all nodes that have boon resolved
  this includes the facts + every nodes that needs to be resolved to answer a query
  attributes:
    _nodes ==> {}
    _rules ==> {}
    _facts ==> []
  """

  def __init__(self, facts, rules):
    self._nodes = {}
    for fact in facts:
      node = Node(fact, [])
      node._value = True
      self.add_node(node)
    self._rules = rules
    self._facts = facts

  def add_node(self, node):
    """
    syntaxic sugar function
    """
    self._nodes[node._name] = node

  def or_operation(self, left, right):
    """==> left | right """
    return (left or right)

  def xor_operation(self, left, right):
    """==> left ^ right """
    return (left != right)

  def and_operation(self, left, right):
    """==> left + right """
    return (left and right)

  def error():
    print('ERROR CUT ALL SHIT')

  def resolve_premisse_value(self, premisse, parents):
    """
    a premisse is either a token or an object( a graph that reprensents a complex premisse)
    note that EVERY complex premisse can be break down into tokens+operators by recursivity
    cf :
    {'|': [A, B]}  --- > a complex premisse
    !A --- > a token
      this function takes a premisse
      and solve it either it's a complex or not

      this func also keeps tracks of the chain of premisses that lead to a premisse (cf: parents)
      because, as it is recursive, we could fall into an infinite loop
      cf :
      A => B
      B => A
      ?A

    """
    if Token.is_token(premisse):
      if parents and premisse in parents:
        return None
      return self.resolve_node(premisse, parents + [premisse])
    else:
      return self.resolve_complex_premisse(premisse, parents + [premisse])

  def resolve_complex_premisse(self, premisse, parents):
    """
    this function is used to solve complex premisse
    it links values of left and right member of a premisse with their main operator

    this is where the recursion happens
    """
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
    # need only one True to determine that Node value is True
    # but need all wrongs to determine that Node value is None
      if self.resolve_premisse_value(premisse, parents):
        value = True
        break
    return value

  def resolve_node(self, name, parents = []):
    """
      this function is just a wrapper
      for resolve_node_value
      it prevents from solving many times the same node
    """
    if name in self._nodes:
      return self._nodes[name]._value
    else:
      node = Node(name, self._rules[name] if name in self._rules else [])
      value = self.resolve_node_value(node, parents)
      node._value = value
      self.add_node(node)
      return value

  def resolve_query(self, query):
    """
      this function receives a query,
      will look for its node and anti_node value
      and make a synthese of combined results
    """
    anti_query = ''
    if query[0] == '!':
      anti_query = query[1:]
    else:
      anti_query = '!' + query
    node_value = self.resolve_node(query, parents)
    anti_node_value = self.resolve_node(anti_query)
    if node_value != anti_node_value:
      return str(node_value)
    else:
      return ('unknown') if not node_value else Error('resolve query', 'contradiction with {}'.format(query))
