#!/usr/bin/python3

import sys
import re

from parser import Parser

output = []
pile = []
operators = ['+', '|', '^']

def is_operator(token):
  return(token in operators)

def is_open_parenthesis(token):
  return(token == '(')

def is_close_parenthesis(token):
  return(token == ')')

def handle_operator(token):
  if pile:
    to_compare = pile[-1]
  if not pile or is_open_parenthesis(to_compare) or has_priority(token, to_compare):
    pile.append(token)
  else:
    output.append(pile.pop())
    pile.append(token)

def handle_close_parenthesis():
  while is_open_parenthesis(pile[-1]) is not True:
    output.append(pile.pop())
  pile.pop()

def has_priority(token, to_compare):
  return(operators.index(token) < operators.index(to_compare))

def from_tokens_to_postfix(tokens):
  for token in tokens:
    if is_operator(token):
      handle_operator(token)
    elif is_open_parenthesis(token):
      pile.append(token)
    elif is_close_parenthesis(token):
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
    if is_operator(token):
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

def from_tokens_to_graph(tokens):
  return from_postfix_to_graph(from_tokens_to_postfix(tokens))

def from_string_to_graph(string):
  return from_postfix_to_graph(from_tokens_to_postfix(Parser.parse_string_to_token(string)))

if __name__ == '__main__':
  input_string = sys.argv[1]
  tokens = Parser.parse_string_to_token(input_string)
  postfix = from_tokens_to_postfix(tokens)
  graphed_generated = from_postfix_to_graph(postfix)
  print('graphe generated --- ', graphed_generated)

