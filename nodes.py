#!/usr/bin/python3

from rpn import from_string_to_graph

class Node:
  """
  A node is a fact verified or not.
  It can have 0 or more graphs that leads to the fact himself
  """

  _name = ''
  _premisses = []
  _value = None
  _parents = []
  _is_child = None
  _is_negation = None

  def __init__(self, name, premisses, parents = []):
    self._name = name
    self._is_child = True if parents else None
    self._is_negation = True if name[0] == '!' else None
    self._parents = parents
    for premisse in premisses:
      self._premisses.append(from_string_to_graph(premisse))
    print('node ', self._name, ' has as premisses : ', self._premisses)
