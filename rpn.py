#!/usr/bin/python3

import sys
import re

from parser import Parser
from tokens import Token
from parse_error import ParseError
from file_error import FileError
from termcolor import colored

def handle_operator(token, output, pile):
  if pile:
    to_compare = pile[-1]
  if not pile or to_compare.is_open_parenthesis() or token.has_priority_on(to_compare):
    pile.append(token)
  else:
    output.append(pile.pop())
    pile.append(token)

def handle_close_parenthesis(output, pile):
  while pile and pile[-1].is_open_parenthesis() is not True:
    output.append(pile.pop())
  if pile:
    pile.pop()
  else:
    raise ParseError('-no corresponding parenthesis')


def from_tokens_to_postfix(tokens):
  output = []
  pile = []
  for token in tokens:
    if token.is_operator():
      handle_operator(token, output, pile)
    elif token.is_open_parenthesis():
      pile.append(token)
    elif token.is_close_parenthesis():
      handle_close_parenthesis(output, pile)
    else:
      output.append(token)
    #print('cur token :', token, ' cur pile: ', pile, ' cur output: ', output)
  if '(' in pile:
    raise ParseError('- open parenthesis not closed')
  output.extend(list(reversed(pile)))
  return output

def from_postfix_to_graph(postfix):
  """
  ['a', 'b', '+', 'C', '|']
  should become:
    {
  	'|': [ 'C', {
  				'+': ['A', 'B']
  				} ]
  	}
  """
  operandes = []
  if len(postfix) <= 1:
    if isinstance(postfix[0], Token) and postfix[0].is_operator():
        raise ParseError('only one operator')
    else:
      return postfix.pop() if postfix else {}
  for index, token in enumerate(postfix):
    if isinstance(token, Token) and token.is_operator():
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
      operandes.append({ token: [operandes.pop(), operandes.pop()] })
      return from_postfix_to_graph(operandes + postfix[index + 1:])
    else:
      operandes.append(token)

def from_tokens_to_graph(tokens):
  return from_postfix_to_graph(from_tokens_to_postfix(tokens))

def from_string_to_graph(string):
  try:
    return from_postfix_to_graph(from_tokens_to_postfix(Parser.parse_string_to_token(string)))
  except ParseError as exception:
    print(colored('Parse error of type : {} detected on line\n\t --> {}'.format(exception.exception_type, string), 'red'))
    raise FileError()
