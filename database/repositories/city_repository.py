from core.database.repository import Repository
from database.models.city import City

from sqlalchemy import func

class CityRepository(Repository):
    pass

    def getAll(self):
        return self.session.query(City).all()

    def getByName(self, name):
        name = name[1:-1]
        return self.session.query(City).filter(func.upper(City.name) == name.upper()).first()