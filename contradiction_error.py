#!/usr/bin/python3

class ContradictionError(Exception):
  """class that handle contradictions and explains it"""

  def __init__(self, name, value):
    self.name = name
    self.value = value
