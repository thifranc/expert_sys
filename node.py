class Node(object):
  """
  A node is a fact verified or not.
  It can have 0 or more graphs that leads to the fact himself
  """

  _instances = {}

  @classmethod
  def get_instance(cls, name):
    if name in Node._instances:
      return Node._instances[name]

  def __new__(cls, name):
    print("new node : ", name)
    node = Node.get_instance(name)
    if node:
      return node
    print("new node create : ", name)
    Node._instances[name] = super(Node, cls).__new__(cls)
    return Node._instances[name]

  def __init__(self, name):
    """Returns a Node instance if one exists with the same name, creates a new instance if not"""
    print("init node : ", name)
    self.name = name

  def __str__(self):
    return('Node : {0}'.format(self.name))

  def __repr__(self):
    return('<Node :  name => {}>'.format(self.name))
