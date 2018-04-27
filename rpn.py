#!/usr/bin/python3

import sys
import re

from parser import Parser
from token import Token

output = []
pile = []

def handle_operator(token):
  if pile:
    to_compare = pile[-1]
  if not pile or to_compare.is_open_parenthesis() or token.has_priority_on(to_compare):
    pile.append(token)
  else:
    output.append(pile.pop())
    pile.append(token)

def handle_close_parenthesis():
  while pile[-1].is_open_parenthesis() is not True:
    output.append(pile.pop())
  pile.pop()


def from_string_to_rpn(tokens):
  for token in tokens:
    if token.is_operator():
      handle_operator(token)
    elif token.is_open_parenthesis():
      pile.append(token)
    elif token.is_close_parenthesis():
      handle_close_parenthesis()
    else:
      output.append(token)
    print('cur token :', token, ' cur pile: ', pile, ' cur output: ', output)
  output.extend(list(reversed(pile)))
  return output

"""
['a', 'b', '+', 'C', '|']
should become:
  {
	'|': [ 'C', {
				'+': ['A', 'B']
				} ]
	}
"""
def from_postfix_to_graph(postfix):
  operandes = []
  operationItem = {}
  list_len = len(postfix)
  if list_len == 0:
    return {}
  elif list_len == 1:
    return postfix.pop()
  for index, token in enumerate(postfix):
    if isinstance(token, Token) and token.is_operator():
      if not operationItem:
        """
        we will take last two operands on stack and affiliate them with current operator
         e.g. : postfix = [a, b, c, +, ^]
         operandes appends until '+', where operands=[a, b, c]
         operation is b+c => { '+': [b,c] }
         operands is now = [ a ]
         we append to it new operand (which is operationItem created)
         then we craft a new array to have a recursion call with:
         [a, { '+': [b,c] }, ^]
        """
        operationItem = { token: [operandes.pop(), operandes.pop()] }
      else:
        print('operator item exist but should not ----- ', operationItem)
      operandes.append(operationItem)
      return from_postfix_to_graph(operandes + postfix[index + 1:])
      break
    else:
      operandes.append(token)

if __name__ == '__main__':
  input_string = sys.argv[1]
  parsed = from_string_to_rpn(Parser.parse_string_to_token(input_string))
  print('we have a new parsed string --- ', parsed);
  graph_generated = from_postfix_to_graph(parsed)
  print('we have a new graph --- ', graph_generated);

