from core.database.repository import Repository

from database.models.user import User
from database.models.city import City
from database.models.label import Label
from database.models.restriction import Restriction
from database.models.subscription import Subscription

from sqlalchemy.dialects import mysql

class UserRepository(Repository):   

    def first(self):
        return self.session.query(User).first()

    def all(self):
        return self.session.query(User).all()
    
    def last(self):
        return self.session.query(User).order_by(User.id.desc()).first()

    def getUsers(self, city = None):
        if city is not None:
            return self.session.query(User).join(Subscription).join(Restriction).filter(User.isActive == True).filter(Subscription.isActive == True).filter(Subscription.cityId == city.id).all()
        else:
            return self.session.query(User).join(Subscription).join(Restriction).filter(User.isActive == True).filter(Subscription.isActive == True).all()

    def get(self, user):
        userDb = self.session.query(User).filter(User.telegram == user.id).first()
        if userDb is None:
            userDb = self.session.query(User).filter(User.id == user.id).filter(User.isActive == True).first()

        return userDb

    def subscribe(self, user):
        userDb = User()
        userDb.name = user.first_name
        userDb.surname = user.last_name
        userDb.telegram = user.id
        user.isActive = False
        return self.save(userDb)
        self.session.commit()

    def unsubscribe(self, user):
        user.isActive = False
        self.save(user)
        self.session.commit()

    def matchesForUsers(self, apartment):
        return self.session.query(User).join(Subscription).join(Restriction).filter(Restriction.minRooms <= int(apartment.rooms)).filter(Restriction.minSurface <= int(apartment.surface)).filter(Restriction.maxPrice >= int(apartment.price)).all()

    def getUsersOnCityLabel(self, city, label):
        return self.session.query(User).join(Subscription).join(City).filter(User.isActive == True).filter(Subscription.isActive == True).filter(City.name == city.name).filter(Label.name == label.name).all()