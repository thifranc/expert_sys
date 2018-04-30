#!/usr/bin/python3

from rpn import from_string_to_graph

class Node:
  """
  A node is a token verified or not.
  It can have 0 or more premisses that leads to the token itself
  """

  _name = ''
  _premisses = []
  _value = None
  #_is_negation = None

  def __init__(self, name, premisses):
    self._premisses = []
    self._value = None
    #_is_negation = None   -> useless so far
    self._name = name
    #self._is_negation = True if name[0] == '!' else None
    for premisse in premisses:
      self._premisses.append(from_string_to_graph(premisse))
    #print('node ', self._name, ' has as premisses : ', self._premisses)
