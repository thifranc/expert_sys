#!/usr/bin/python3

from node import Node
from tokens import Token
from contradiction_error import ContradictionError
from file_error import FileError
from termcolor import colored

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

  def __init__(self, facts, rules, verbose = None):
    self._nodes = {}
    for fact in facts:
      node = Node(fact, [])
      node._value = True
      self.add_node(node)
    self._rules = rules
    self._facts = facts
    self._verbose = verbose

  def add_node(self, node):
    """
    syntaxic sugar function
    """
    self._nodes[node._name] = node

  def get_anti_query(self, query):
    """
    convenience function
    """
    if query[0] == '!':
      return query[1:]
    else:
      return '!' + query

  def or_operation(self, left, right):
    """==> left | right """
    return (left or right)

  def xor_operation(self, left, right):
    """==> left ^ right """
    return (left != right)

  def and_operation(self, left, right):
    """==> left + right """
    return (left and right)

  def error(self):
    raise FileError('unknown_operator')

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
        if self._verbose:
          print(colored("Infinite loop detected. Will resolve to unknown", 'magenta'))
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
    for premisse in node._premisses:
    # need only one True to determine that Node value is True
    # but need all wrongs to determine that Node value is None
      if self.resolve_premisse_value(premisse, parents):
        return True

  def resolve_node(self, name, parents = [], anti_test = None):
    """
      this function is just a wrapper
      for resolve_node_value
      it prevents from solving many times the same node
    """
    if name in self._nodes:
      ret = 'Value of node {} has already been found.'.format(name) # verbose
      value = self._nodes[name]._value
    else:
      ret = 'trying to resolve node {}.'.format(name) # verbose
      node = Node(name, self._rules[name] if name in self._rules else []) # verbose
      ret += '\nnode premisses are : ' # verbose
      for premisse in node._premisses: # verbose
        ret += "\n{}".format(premisse) # verbose
      value = self.resolve_node_value(node, parents)
      node._value = value
      self.add_node(node)
    if not anti_test:
      anti_value = self.resolve_node(self.get_anti_query(name), parents + [ name ], True)
      if value and anti_value:
        if self._verbose:
          print(ret) # print for debug
        raise ContradictionError(name, value)
    if self._verbose:
      print(ret, '\nreturning ==> ', value, '\n') # verbose
    return value

  def resolve_query(self, query):
    """
      this function receives a query,
      will look for its node and anti_node value
      and make a synthese of combined results
    """
    anti_query = self.get_anti_query(query)
    node_value = self.resolve_node(query, [], True)
    anti_node_value = self.resolve_node(anti_query, [], True)
    if not node_value and anti_node_value:
      return 'false'
    elif node_value and not anti_node_value:
      return 'true'
    elif not node_value and not anti_node_value:
      return 'unknown'
    else:
      raise ContradictionError(query, node_value)
