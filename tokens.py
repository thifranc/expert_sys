
import re

class Token(str):
  """middleware class that handle all simple functions of tokens"""

  operators = ['+', '|', '^']

  tokenPurePattern = re.compile('^!?[a-z]{1}|[+|^()]{1}$', re.I)

  @classmethod
  def is_token(cls, token):
    # isTokenPattern = re.compile('!?[a-z]', re.I)
    return True if isinstance(token, str) else None

  @classmethod
  def token_are_the_same_type(self, token1, token2):
    return (None if (not token1 or not token2) else (token1.is_operator() and token2.is_operator()))

  def __init__(self, token):
    if not self.tokenPurePattern.match(token):
      Error('TOKEN_INIT', '-bad token ' + token)
    else:
      self.token = token

  def is_operator(self):
    return(self.token in Token.operators)

  def is_open_parenthesis(self):
    return(self.token == '(')

  def is_close_parenthesis(self):
    return(self.token == ')')

  def has_priority_on(self, to_compare):
    return(Token.operators.index(self.token) < Token.operators.index(to_compare))
