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

if __name__ == '__main__':
  tokens = sys.argv[1]

  for token in tokens:
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

