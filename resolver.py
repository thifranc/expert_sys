#!/usr/bin/python3

from nodes import Node

class Resolver:

  _nodes = []

  def __init__(self, facts, rules, query):
    print('will resolve ', query, facts)
    if query in facts:
      #print('lol iz')
    else:
      self._node_to_resolve = Node(query, rules[query] if query in rules else [])
      self._nodes.append(self._node_to_resolve)
