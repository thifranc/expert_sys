
import re

class Token(str):
  """middleware class that handle all simple functions of tokens"""

  operators = ['+', '|', '^']

  @classmethod
  def is_token(cls, token):
    # isTokenPattern = re.compile('!?[a-z]', re.I)
    return True if isinstance(token, str) else None

  def __init__(self, token):
    self.token = token

  def is_operator(self):
    return(self.token in Token.operators)

  def is_open_parenthesis(self):
    return(self.token == '(')

  def is_close_parenthesis(self):
    return(self.token == ')')

  def has_priority_on(self, to_compare):
    return(Token.operators.index(self.token) < Token.operators.index(to_compare))
