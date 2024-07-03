from database.DAO import DAO
from model.model import Model

mymodel = Model()

y = DAO.getYears()
c = DAO.getColors()
m = mymodel.getYears()
p = DAO.getAllNodes("Light Blue")

print(len(y))
print(len(c))
print(c)
