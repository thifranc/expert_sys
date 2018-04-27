class Token(str):
  """middleware class that handle all simple functions of tokens"""

  operators = ['+', '|', '^']

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
