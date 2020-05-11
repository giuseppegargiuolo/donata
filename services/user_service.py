from database.models.user import User
from core.services.service import Service
from database.repositories.user_repository import UserRepository

class UserService(Service):

    def getUsers(self, city=None):
        if city is None:
            return self.db.users.getUsers()
        else:
            return self.db.users.getUsers(city)

    def restoreMatches(self, user):
        matches = self.db.matches.getAllByUser(user)

    def getUser(self, *args):
        pass

    def get(self, user):
        return self.db.users.get(user)

    def subscribe(self, user):
        return self.db.users.subscribe(user)

    def unsubscribe(self, user):
        self.db.users.unsubscribe(user)

    def anyUsersOnCityLabel(self, city, label):
        return self.db.users.getUsersOnCityLabel(city, label)