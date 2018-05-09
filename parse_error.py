#!/usr/bin/python3

class ParseError(Exception):
  """class that handle contradictions and explains it"""

  def __init__(self, exception_type = '', message = ''):
    self.exception_type = exception_type
    self.message = message

  def __str__(self):
    return (self.message)
