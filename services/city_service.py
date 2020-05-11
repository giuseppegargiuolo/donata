from core.services.service import Service

class CityService(Service):

    def get(self, city):
        return self.db.cities.getByName(city)

    def all(self):
        return self.db.cities.getAll()