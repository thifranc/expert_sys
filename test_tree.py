from pptree import *

class Employee(object):

  def __init__(self, fullname, function, head=None):
    self.fullname = fullname
    self.function = function
    self.team = []
    if head:
        head.team.append(self)

  def  __str__(self):
      return  self.function

jean = Employee("Jean Dupont", "CEO")
isabelle = Employee("Isabelle Leblanc", "Sales", jean)
enzo = Employee("Enzo Riviera", "Technology", jean)
lola = Employee("Lola Monet", "RH", jean)
kevin = Employee("Kevin Perez", "Developer", enzo)
lydia = Employee("Lydia Petit", "Tester", enzo)

print_tree(jean, "team")
print_tree(jean, "team", "fullname")
