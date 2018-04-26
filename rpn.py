#!/usr/bin/python3

import sys
import re

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
  to_compare = pile[-1] if pile else token
  if is_open_parenthesis(to_compare) or has_priority(token, to_compare):
    pile.append(token)
  else:
    output.append(pile.pop())
    pile.append(token)

def handle_close_parenthesis():
  while is_open_parenthesis(pile[-1]) is not True:
    output.append(pile.pop())
  pile.pop()

def has_priority(token, to_compare):
  return(operators.index(token) <= operators.index(to_compare))

def from_string_to_rpn(string):
  for token in tokens:
    print('cur token -- ', token, '\npile - ', pile, '\noutput', output)
    if is_operator(token):
      handle_operator(token)
    elif is_open_parenthesis(token):
      pile.append(token)
    elif is_close_parenthesis(token):
      handle_close_parenthesis()
    else:
      output.append(token)
  output.extend(list(reversed(pile)))
  print(output)

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
  print('tab received at call - ', postfix)
  list_len = len(postfix)
  if (list_len == 0):
    return {}
  elif len(postfix) == 1:
    return postfix.pop()
  for index, token in enumerate(postfix):
    if is_operator(token):
      if not operationItem:
        operationItem = { token: list(operandes) }
      else:
        print('operator item exist but should not ----- ', operationItem)
      newTab = postfix[index + 1:]
      print('newTab sliced is --- ', newTab)
      newTab.insert(0, operationItem)
      return from_postfix_to_graph(newTab)
      break
    else:
      operandes.append(token)

if __name__ == '__main__':
  graphed_generated = from_postfix_to_graph(['a', 'b', '+', 'C', '|']) #gives: {'+': ['a', 'b'], '|': ['C']}
  print('we have a new graph --- ', graphed_generated);
  #tokens = sys.argv[1]
  #from_string_to_rpn(tokens)

